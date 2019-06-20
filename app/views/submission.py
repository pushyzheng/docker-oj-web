# encoding:utf-8
from app import app, db
from app.models import Submission, JudgementStatus

from flask import jsonify


@app.route('/submission/<id>', methods=['GET'])
def submission(id):
    submission = Submission.query.filter_by(id=id).first()
    if not submission:
        return jsonify(data=None), 404

    resp = jsonify(data=submission.to_dict())
    return resp
