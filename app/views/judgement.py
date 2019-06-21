# encoding:utf-8
from app import app, rabbitmq, db
from app.models import Problem, Submission, JudgementTask
from app.utils import get_uuid
import os
from flask import request, jsonify


@app.route('/judge', methods=['POST'])
def judge():
    code = request.json.get('code')
    user_id = request.json.get('user_id')
    language = request.json.get('language')
    problem_id = request.json.get('problem_id')
    if problem_id:
        problem_id = int(problem_id)

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
