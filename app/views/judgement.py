# encoding:utf-8
from app import app, rabbitmq, db
from app.models import *
import uuid
import os
from flask import request


@app.route('/judge', methods=['POST'])
def judge():
    code = request.json.get('code')
    user_id = request.json.get('user_id')
    language = request.json.get('language')
    problem_id = request.json.get('problem_id')

    user_path = 'e:/usr/pushy/{}'.format(user_id)

    if not os.path.exists(user_path):
        os.mkdir(user_path)

    with open('{}/{}'.format(user_path, get_file_name(language)), 'w', encoding='utf-8', ) as f:
        f.write(code)

    task_id = str(uuid.uuid4()).replace('-', '')
    task = JudgementTask(
        task_id=task_id,
        problem_id=problem_id,
        user_id=user_id,
        language=language
    )
    submission = Submission(
        id=task_id,
        user_id=user_id,
        problem_id=problem_id,
        language=language,
    )
    db.session.add(submission)
    db.session.commit()

    rabbitmq.send(body=task.to_json_string(), exchange='', key='go-docker-judger')

    return 'The task has be committed', 202


def get_file_name(language):
    if language == 'java':
        return 'Main.java'
    if language == 'c':
        return 'main.c'
    if language == 'cpp':
        return 'main.cpp'
    if language == 'py':
        return 'main.py'
