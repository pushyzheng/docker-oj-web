# encoding:utf-8
from app import db
from datetime import datetime
from utils import ModelParent


class Problem(db.Model, ModelParent):
    __tablename__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    time_limit = db.Column(db.Integer)
    memory_limit = db.Column(db.Integer)

    author = db.Column(db.String(32), db.ForeignKey("users.id"))

    timestamp = db.Column(db.DateTime, default=datetime.now)