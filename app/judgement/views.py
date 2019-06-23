# encoding:utf-8
from app import app, rabbitmq, db
from app.problem.models import Problem
from app.submission.models import Submission
from app.judgement.models import JudgementTask
from utils import get_uuid, logger
import os
from flask import jsonify, g
from flask_expects_json import expects_json

schema = {
    'type': 'object',
    'properties': {
        'code': {'type': 'string'},
        'user_id': {'type': 'string'},
        'language': {'type': 'string'},
        'problem_id': {'type': 'integer'}
    },
    'required': ['code', 'user_id', 'language', 'problem_id']
}


@app.route('/judge', methods=['POST'])
@expects_json(schema)
def judge():
    data = g.data
    code = data['code']
    user_id = data['user_id']
    language = data['language']
    problem_id = data['problem_id']

    problem = Problem.query.filter_by(id=problem_id).first()
    if not problem:
        return jsonify(data=None, message='The problem not found'), 404

    user_path = 'e:/usr/pushy/{}'.format(user_id)

    if not os.path.exists(user_path):
        os.mkdir(user_path)

    with open('{}/{}'.format(user_path, get_file_name(language)), 'w', encoding='utf-8') as f:
        f.write(code)

    task_id = get_uuid()
    task = JudgementTask(
        task_id=task_id,
        problem_id=problem_id,
        user_id=user_id,
        language=language,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit
    )
    submission = Submission(
        id=task_id,
        user_id=user_id,
        problem_id=problem_id,
        language=language,
        code=code
    )
    resp = submission.to_dict()
    db.session.add(submission)
    db.session.commit()

    logger.info("Send task => {}".format(task))
    rabbitmq.send(body=task.to_json_string(), exchange='', key='go-docker-judger')

    return jsonify(data=resp), 202


def get_file_name(language):
    if language == 'java':
        return 'Main.java'
    if language == 'c':
        return 'main.c'
    if language == 'cpp':
        return 'main.cpp'
    if language == 'py':
        return 'main.py'
