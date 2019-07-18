# encoding:utf-8
from app import app, db
from flask import g, abort
from app.submission.models import Submission
from app.common.models import JudgementStatus
from app.common.user import User
from utils import success, get_day_zero_time
from datetime import datetime, timedelta
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


@app.route('/rank/week')
def get_week_rank():
    now = datetime.now()
    zero_time = get_day_zero_time(now)
    start = zero_time - timedelta(days=zero_time.weekday()) # 本周起始时间
    start_str = '{0:%Y-%m-%d %H:%M:%S}'.format(start)
    now_str = '{0:%Y-%m-%d %H:%M:%S}'.format(now)

    sql = """
    select u.id, u.username, u.avatar_url, count(*) from 
        submissions s left join users u on u.id = s.user_id 
            where s.timestamp > '{}' and s.timestamp < '{}' and s.result = 0 group by s.user_id;
    """.format(start_str, now_str)

    cursor = db.session.execute(sql)
    result_set = cursor.fetchall()

    result = []
    for row in result_set:
        result.append({
            'id': row[0],
            'username': row[1],
            'avatar_url': row[2],
            'count': row[3]
        })

    if len(result) < 3:
        for i in range(3 - len(result)):
            result.append({
                'id': None,
                'username': '暂无人选',
                'avatar_url': None,
                'count': 0
            })
    return success(result)
