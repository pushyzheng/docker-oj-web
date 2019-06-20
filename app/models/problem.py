# encoding:utf-8
from app import db
from datetime import datetime


class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.String(32), primary_key=True, nullable=True)
    title = db.Column(db.String(32), nullable=True)
    content = db.Column(db.Text, nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.now)