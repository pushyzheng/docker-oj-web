# encoding:utf-8
from app import app
from app.common.user import User
from flask import abort, g, request, session
from utils import logger
from app.common.models import RoleName
import json
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


# @app.before_request
# def before_request():
#     g.token = request.headers.get('token')

def auth(role=RoleName.USER):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # if user in session, then don't decode token
            if session.get('user'):
                user = User()
                user.from_dict(session.get('user'))
                if not can_visit(user, role):
                    abort(403, 'No permission!')
                g.user = user
                return func(*args, **kwargs)

            token = request.headers.get('token')
            if not token:
                raise abort(401, 'Token is not present.')
            s = Serializer(app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
                # query user and set user object to session
                user = User.query.filter_by(id=data['id']).first()
                if not can_visit(user, role):
                    abort(403, 'No permission!')
                g.user = user

                session['user'] = user.to_dict()

            except SignatureExpired:
                raise abort(401, 'Token expired, please login again')
            except BadSignature:
                raise abort(401, '认证失败')
            except Exception as e:
                logger.error(e)
                abort(500, str(e))

            return func(*args, **kwargs)
        return wrapper
    return decorator


def can_visit(user, role):
    if RoleName.get_weight_by_name(user.role) < RoleName.get_weight_by_name(role):
        return False
    return True
