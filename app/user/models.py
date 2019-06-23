# encoding:utf-8
from app import db
from utils import ModelParent
from datetime import datetime


class User(db.Model, ModelParent):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # submissions = db.relationship('Submission', backref='user', lazy='dynamic')
    problems = db.relationship('Problem', backref='user', lazy='dynamic')
