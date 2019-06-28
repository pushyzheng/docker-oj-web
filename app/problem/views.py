# encoding:utf-8
from app import app, db
from app.problem.models import Problem
from app.submission.models import Submission, JudgementStatus
from utils import success, logger
from flask import abort
from sqlalchemy import and_


@app.route('/problems', methods=['GET'])
def list_problem():
    problem_list = Problem.query.all()

    resp = []
    for problem in problem_list:
        passing_submissions = Submission.query.filter(and_(
            Submission.problem_id == problem.id,
            Submission.result == JudgementStatus.ACCEPTED)).all()
        all_submissions = Submission.query.filter_by(problem_id=problem.id).all()

        if len(all_submissions) != 0:
            passing_rate = len(passing_submissions) / len(all_submissions)
            problem.passing_rate = round(passing_rate, 2)
        else:
            problem.passing_rate = 0

        problem_dict = problem.to_dict()
        problem_dict['key'] = problem.id
        resp.append(problem_dict)

        db.session.add(problem)  # 暂存

    db.session.commit()
    return success(resp)


@app.route('/problems/<id>', methods=['GET'])
def get_problem_by_id(id):
    problem = Problem.query.filter_by(id=id).first()
    if not problem:
        abort(404, 'The problem is not found')

    return success(problem.to_dict())


@app.route('/problems/hot', methods=['GET'])
def get_hot_problem():
    sql = """
        SELECT s.problem_id, p.title, p.difficulty, p.passing_rate, count(*) count 
            FROM submissions s 
            LEFT JOIN problems p ON p.id = s.problem_id GROUP BY s.problem_id;
    """
    cursor = db.session.execute(sql)
    result_set = cursor.fetchall()

    result = []
    for row in result_set:
        result.append({
            'id': row[0],
            'title': row[1],
            'difficulty': row[2],
            'passing_rate': '{} %'.format(round(row[3], 2) * 100),
            'count': row[4]
        })
    return success(result)