# encoding:utf-8
from app import app
from flask import g, abort
from app.submission.models import Submission
from app.common.models import JudgementStatus
from app.common.user import User
from utils import success
from sqlalchemy import and_


@app.route('/rank')
def get_rank():
    user_list = User.query.all()
    user_dict = {}
    user_ac_count = {}

    for user in user_list:
        user_dict[user.id] = user.to_public_dict()

        submissions = Submission.query.filter(and_(
            Submission.user_id == user.id, Submission.result == JudgementStatus.ACCEPTED
        )).all()
        user_ac_count[user.id] = len(submissions)

    items = sorted(user_ac_count.items(), key=lambda item: item[1], reverse=True)

    resp = []
    for item in items:
        submissions = Submission.query.filter_by(user_id=item[0]).all()
        resp.append({
            'user': user_dict[item[0]],
            'ac_count': item[1],
            'submissions_count': len(submissions)
        })

    return success(resp)
