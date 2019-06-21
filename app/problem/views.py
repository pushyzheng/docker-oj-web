# encoding:utf-8
from app import app, db
from app.problem.models import Problem
from utils import get_uuid
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
