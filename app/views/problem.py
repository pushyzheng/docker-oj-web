# encoding:utf-8
from app import app, db
from app.models import Problem
from app.utils import get_uuid
from flask import request, jsonify


@app.route('/problems', methods=['GET'])
def list_problem():
    problem_list = [each.to_dict() for each in Problem.query.all()]
    return jsonify(
        data=problem_list
    )


@app.route('/problems/<id>', methods=['GET'])
def get_problem_by_id(id):
    problem = Problem.query.filter_by(id=id).first()
    return jsonify(
        data=problem.to_dict()
    )


@app.route('/problems', methods=['POST'])
def save_problem():
    user_id = 123

    id = get_uuid()
    title = request.json.get('title')
    content = request.json.get('content')
    time_limit = request.json.get('time_limit')
    memory_limit = request.json.get('memory_limit')

    problem = Problem(
        id=id,
        title=title,
        content=content,
        time_limit=time_limit,
        memory_limit=memory_limit,
        author=user_id
    )
    resp = problem.to_dict()

    db.session.add(problem)
    db.session.commit()

    return jsonify(data=resp)