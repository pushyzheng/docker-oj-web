# encoding:utf-8
from app import app, db
from app.problem.models import Problem
from flask import jsonify, g
from flask_expects_json import expects_json
from sqlalchemy import desc

schema = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'content': {'type': 'string'},
        'time_limit': {'type': 'integer'},
        'memory_limit': {'type': 'integer'}
    },
    'required': ['title', 'content', 'time_limit', 'memory_limit']
}


@app.route('/admin/problems', methods=['POST'])
@expects_json(schema)
def save_problem():
    problem = Problem()
    problem.from_dict(g.data)

    problem.id = get_problem_id()
    problem.author = 123

    resp = problem.to_dict()

    db.session.add(problem)
    db.session.commit()

    return jsonify(data=resp)


def get_problem_id():
    problem = Problem.query.order_by(desc(Problem.id)).first()
    if not problem:
        return 1
    return problem.id + 1