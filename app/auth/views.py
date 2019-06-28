# encoding:utf-8
from app import app, db
from app.common.models import RoleName
from utils import success, get_uuid, logger, get_avatar_url
from schemas.auth import *
from app.common.user import User
from app.auth.main import auth
from flask import g, abort, session, request
from flask_expects_json import expects_json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@app.route('/login', methods=['POST'])
@expects_json(login_schema)
def login():
    username, password = g.data['username'], g.data['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404, 'The user not found')
    if user.password != password:
        abort(401, 'Fail to login, please check your username and password')

    s = Serializer(app.config['SECRET_KEY'], expires_in=1 * 2592000)
    resp = {
        'access_token': str(s.dumps({'id': user.id}), encoding='utf-8'),
        'user': user.to_dict()
    }

    session['user'] = user.to_dict()

    return success(resp)


@app.route('/register', methods=['POST'])
@expects_json(register_schema)
def register():
    username, password = g.data['username'], g.data['password']
    email = g.data['email']

    user = User.query.filter_by(username=username).first()
    if user:
        abort(400, '用户名已存在')
    user = User.query.filter_by(email=email).first()
    if user:
        abort(400, '邮箱已存在')

    user_id = get_uuid()
    user = User(
        id=user_id,
        username=username,
        password=password,
        email=email,
        avatar_url=get_avatar_url(email)
    )
    resp = user.to_dict()

    db.session.add(user)
    db.session.commit()

    return success(resp)


@app.route('/logout', methods=['POST'])
@auth(role=RoleName.USER)
def logout():
    if session.get('user'):
        session.pop('user')
    return success()


@app.route('/token', methods=['GET'])
def valid_token():
    token = request.args.get('token')
    result = False
    if token:
        try:
            s = Serializer(app.config['SECRET_KEY'])
            s.loads(token)
            result = True
        except Exception:
            pass
    return success(result)


@app.route('/role', methods=['GET'])
@auth(role=RoleName.USER)
def get_role():
    return success({
        'role_name': g.user.role
    })
