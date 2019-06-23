# encoding:utf-8
from app import app
from app.submission.models import Submission, JudgementStatus
from flask import abort
from sqlalchemy import desc
from utils import sort_and_distinct, success


@app.route('/submissions/<id>', methods=['GET'])
def submission(id):
    sub = Submission.query.filter_by(id=id).first()
    if not sub:
        abort(404, 'The submission not found.')

    if sub.result == JudgementStatus.ACCEPTED:
        time_rate, memory_rate = count_exceeding_rate(sub)
        setattr(sub, 'time_rate', time_rate)
        setattr(sub, 'memory_rate', memory_rate)

    return success(sub.to_dict())


@app.route('/submissions/latest', methods=['GET'])
def get_latest_submission():
    user_id = 123
    sub = Submission.query.filter_by(user_id=user_id).order_by(desc(Submission.timestamp)).first()
    if not sub:
        return success(None)

    return success(sub.to_dict())


# 计算时间复杂度超过率、空间复杂度超过率
def count_exceeding_rate(sub):
    submissions = Submission.query.filter_by(result=JudgementStatus.ACCEPTED).all()
    time_list = [each.runtime_time for each in submissions]
    memory_list = [each.runtime_memory for each in submissions]

    time_rate = count_rank(time_list, sub.runtime_time)
    memory_rate = count_rank(memory_list, sub.runtime_memory)

    return time_rate, memory_rate


# 计算值在列表中的排名
def count_rank(data_list, val):
    data_list = sort_and_distinct(data_list)
    time_rate = data_list.index(val) / len(data_list)
    return round(time_rate, 2)
