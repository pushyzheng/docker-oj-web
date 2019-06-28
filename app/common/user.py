# encoding:utf-8
from app import db
from utils import ModelParent
from app.common.models import RoleName
from datetime import datetime


class User(db.Model, ModelParent):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    email = db.Column(db.String(32))
    qq = db.Column(db.String(32))
    github = db.Column(db.String(32))

    university = db.Column(db.String(32))
    college = db.Column(db.String(32))
    specialty = db.Column(db.String(32))
    grade = db.Column(db.String(32))

    role = db.Column(db.String(11), default=RoleName.USER)

    timestamp = db.Column(db.DateTime, default=datetime.now)

    # submissions = db.relationship('Submission', backref='user', lazy='dynamic')
    # problems = db.relationship('Problem', backref='user', lazy='dynamic')

    def to_public_dict(self):
        result = self.to_dict()
        result.pop('role')
        result.pop('password')

        return result
