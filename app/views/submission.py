# encoding:utf-8
from app import app, db
from app.models import Submission

from flask import jsonify
from sqlalchemy import desc


@app.route('/submissions/<id>', methods=['GET'])
def submission(id):
    sub = Submission.query.filter_by(id=id).first()
    if not sub:
        return jsonify(data=None), 404

    resp = jsonify(data=sub.to_dict())
    return resp


@app.route('/submissions/latest', methods=['GET'])
def get_latest_submission():
    user_id = 123
    sub = Submission.query.filter_by(user_id=user_id).order_by(desc(Submission.timestamp)).first()
    if not sub:
        return jsonify(data=None)

    resp = jsonify(data=sub.to_dict())
    return resp
