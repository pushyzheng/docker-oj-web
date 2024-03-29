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

    author = db.Column(db.String(32), db.ForeignKey("users.id"))  # 作者
    labels = db.relationship('Label', backref='problem', lazy='dynamic')  # 标签

    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        result = super().to_dict()
        labels = []
        for each in self.labels:
            labels.append(each.name)

        result['labels'] = labels
        return result
