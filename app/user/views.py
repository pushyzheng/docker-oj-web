# encoding:utf-8
from app import app, db
from app.common.models import RoleName, JudgementStatus
from app.common.user import User
from app.submission.models import Submission
from app.auth.main import auth
from utils import logger, success
from datetime import datetime, timedelta
from sqlalchemy import and_, desc
from flask import request, g, abort


@app.route('/users/submissions')
@auth(role=RoleName.USER)
def get_user_submissions():
    problem_id = request.args.get('problem_id')

    submissions = Submission.query.filter(and_(
        Submission.user_id == g.user.id,
        Submission.problem_id == problem_id))

    resp = []
    for sub in submissions:
        sub_dict = sub.to_dict()
        sub_dict.pop('code')
        sub_dict.pop('error_info')
        sub_dict['key'] = sub.id
        sub_dict['result'] = JudgementStatus.get_desc_CN(sub.result)
        resp.append(sub_dict)
    return success(resp)


@app.route('/users/submissions-week')
@auth(role=RoleName.USER)
def get_week_submissions():
    now = datetime.now()
    zero_time = get_day_zero_time(now)
    start = zero_time - timedelta(days=zero_time.weekday())

    # 统计每天的总提交数、通过题数、未通过题数
    day_start = start
    day_end = start + timedelta(days=1)

    week_total = []
    week_ac = []
    week_no_passing = []
    week_list = []
    for i in range(7):
        submissions = Submission.query.filter(
            and_(Submission.user_id == g.user.id,
                 Submission.timestamp.between(day_start, day_end))).order_by(Submission.timestamp).all()
        week_total.append(len(submissions))
        ac_count = 0
        for sub in submissions:
            if sub.result == JudgementStatus.ACCEPTED:
                ac_count += 1
        week_ac.append(ac_count)
        week_no_passing.append(len(submissions) - ac_count)

        if day_start == zero_time:
            week_list.append('今天')
        else:
            week_list.append(get_week_CN(i + 1))

        day_start += timedelta(days=1)
        day_end += timedelta(days=1)

    result = {
        'week_total': week_total,
        'week_ac': week_ac,
        'week_no_passing': week_no_passing,
        'week_list': week_list
    }
    return success(result)


@app.route('/users/profile')
@auth(role=RoleName.USER)
def get_profile():
    return success(g.user.to_public_dict())


@app.route('/users/profile', methods=['PUT'])
@auth(role=RoleName.USER)
def update_profile():
    user = User.query.filter_by(id=g.user.id).first()
    data = request.json
    if not data:
        abort(404, 'json data is empty')

    email = data.get('email')
    qq = data.get('qq')
    github = data.get('github')
    if not empty(email):
        user.email = email
    if not empty(qq):
        user.qq = qq
    if not empty(github):
        user.github = github

    university = data.get('university')
    college = data.get('college')
    specialty = data.get('specialty')
    grade = data.get('grade')
    if not empty(university):
        user.university = university
    if not empty(college):
        user.college = college
    if not empty(specialty):
        user.specialty = specialty
    if not empty(grade):
        user.grade = grade

    result = user.to_public_dict()
    db.session.add(user)
    db.session.commit()
    return success(result)


@app.route('/users/<user_id>/profile')
def get_profile_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404, 'The user not found')

    # 总提交数和AC数
    submissions = Submission.query.filter_by(user_id=user_id).all()
    ac_count = 0
    skill = {}
    for sub in submissions:
        if sub.result == JudgementStatus.ACCEPTED:
            ac_count += 1
        if sub.language not in skill:
            skill[sub.language] = 1
        else:
            skill[sub.language] += 1
    # 通过率
    passing_rate = 0
    if len(submissions) != 0:
        passing_rate = ac_count / len(submissions)

    resp = {
        'ac_count': ac_count,
        'submissions_count': len(submissions),
        'passing_rate': round(passing_rate, 2),
        'user': user.to_public_dict(),
        'skill': skill
    }
    return success(resp)


@app.route('/users/<id>')
@auth(role=RoleName.USER)
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404, 'The user not found')

    return success(user.to_dict())


def get_day_zero_time(date):
    result = datetime.now().replace(year=date.year, month=date.month,
                                    day=date.day, hour=0, minute=0, second=0)
    return result


def get_week_CN(week):
    if week == 1:
        return '周一'
    elif week == 2:
        return '周二'
    elif week == 3:
        return '周三'
    elif week == 4:
        return '周四'
    elif week == 5:
        return '周五'
    elif week == 6:
        return '周六'
    elif week == 7:
        return '周日'


def empty(value):
    if type(value) == int:
        return False

    if not value or len(value) == 0:
        return True
    else:
        return False