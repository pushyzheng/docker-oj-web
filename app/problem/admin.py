# encoding:utf-8
from app import app, db
from app.problem.models import Problem
from utils import logger
from schemas.problem import *
import os
from flask import jsonify, g, abort
from flask_expects_json import expects_json
from sqlalchemy import desc
import requests


@app.route('/admin/problems', methods=['POST'])
@expects_json(save_problem_schema)
def save_problem():
    case_list, answer_list = g.data['case_list'], g.data['answer_list']
    if len(case_list) != len(answer_list):
        abort(400, 'case list length must equals answer list length')

    problem = Problem()
    problem.from_dict(g.data)

    problem.id = get_problem_id()
    problem.author = 123

    # 调用Github接口，渲染题目markdown内容
    problem.content_html = render_markdown_text(problem.content)

    resp = problem.to_dict()

    db.session.add(problem)
    db.session.commit()

    write_case_and_answer_to_file(problem.id, case_list, answer_list)

    return jsonify(data=resp)


@app.route('/admin/problems/<id>', methods=['PUT'])
@expects_json(update_problem_schema)
def update_problem(id):
    problem = valid_exists_problem(id)

    for key in g.data.keys():
        if g.data[key] and g.data[key] != '':
            setattr(problem, key, g.data[key])

    problem.content_html = render_markdown_text(g.data['content'])

    resp = problem.to_dict()

    db.session.add(problem)
    db.session.commit()

    return jsonify(data=resp)


@app.route('/admin/problems/<id>/cases', methods=['GET'])
def get_problem_cases(id):
    valid_exists_problem(id)

    problem_case_path = '{}/case_{}.txt'.format(app.config['CASE_PATH'], id)
    if not os.path.exists(problem_case_path):
        return jsonify(data=None)

    case_list = []
    with open(problem_case_path) as f:
        lines = f.readlines()
        for line in lines:
            case_list.append(line.replace("\n", ""))

    return jsonify(data=case_list)


@app.route('/admin/problems/<id>/answers', methods=['GET'])
def get_problem_answer(id):
    valid_exists_problem(id)

    problem_answer_path = '{}/answer_{}.txt'.format(app.config['ANSWER_PATH'], id)
    if not os.path.exists(problem_answer_path):
        return jsonify(data=None)

    answer_list = []
    with open(problem_answer_path) as f:
        lines = f.readlines()
        for line in lines:
            answer_list.append(line.replace("\n", ""))

    return jsonify(data=answer_list)


@app.route('/admin/problems/<id>/cases-and-answers', methods=['PUT'])
@expects_json(update_cases_answers_schema)
def update_problem_answers(id):
    valid_exists_problem(id)

    case_list, answer_list = g.data['case_list'], g.data['answer_list']
    if len(case_list) != len(answer_list):
        abort(400, 'case list length must equals answer list length')

    # 写入测试样例文件和答案文件中
    write_case_and_answer_to_file(id, case_list, answer_list)

    return jsonify(data=None)


def valid_exists_problem(id):
    problem = Problem.query.filter_by(id=id).first()
    if not problem:
        abort(404, 'The problem not found')

    return problem


def get_problem_id():
    problem = Problem.query.order_by(desc(Problem.id)).first()
    if not problem:
        return 1
    return problem.id + 1


def write_case_and_answer_to_file(problem_id, case_list, answer_list):
    problem_case_path = '{}/case_{}.txt'.format(app.config['CASE_PATH'], problem_id)
    problem_answer_path = '{}/answer_{}.txt'.format(app.config['ANSWER_PATH'], problem_id)

    with open(problem_case_path, 'a', encoding='utf-8') as f:
        for case in case_list:
            f.write(case + '\n')

    with open(problem_answer_path, 'a', encoding='utf-8') as f:
        for answer in answer_list:
            f.write(answer + '\n')


def render_markdown_text(text):
    text = text.encode('utf-8')

    url = "https://api.github.com/markdown/raw"
    headers = {
        "Content-Type": "text/plain"
    }
    response = requests.request("POST", url, data=text, headers=headers)
    return response.text
