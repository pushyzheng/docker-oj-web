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
    time_limit = db.Column(db.Integer)  # 时间限制
    memory_limit = db.Column(db.Integer)  # 内存限制

    passing_rate = db.Column(db.Float)  # 通过率
    difficulty = db.Column(db.String(10))  # 难度

    author = db.Column(db.String(32), db.ForeignKey("users.id"))

    timestamp = db.Column(db.DateTime, default=datetime.now)
