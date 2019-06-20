# encoding:utf-8
from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True, nullable=True)
    username = db.Column(db.String(32), nullable=True)
    password = db.Column(db.String(32), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    submissions = db.relationship('Submission', backref='user', lazy='dynamic')
