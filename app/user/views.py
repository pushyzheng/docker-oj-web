# encoding:utf-8
from app import app
from app.submission.models import Submission
from app.user.models import User
from flask import request, jsonify
from sqlalchemy import and_


@app.route('/users/submissions')
def get_user_submissions():
    user_id = "123"
    problem_id = request.args.get('problem_id')

    submissions = Submission.query.filter(and_(
        Submission.user_id == user_id,
        Submission.problem_id == problem_id))

    return jsonify(data=[sub.to_dict() for sub in submissions])
