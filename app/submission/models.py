# encoding:utf-8
from app import db
from datetime import datetime
from utils import ModelParent


class JudgementStatus:
    COMPILE_ERROR = -2
    WRONG_ANSWER = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    PENDING = 6
    JUDGING = 7
    PARTIALLY_ACCEPTED = 8

    @staticmethod
    def get_status(result):
        if result == "COMPILE_ERROR":
            return -2
        if result == "WRONG_ANSWER":
            return -1
        if result == "ACCEPTED":
            return 0
        if result == "TIME_LIMIT_EXCEED":
            return 2
        if result == "MEMORY_LIMIT_EXCEED":
            return 3
        if result == "RUNTIME_ERROR":
            return 4
        if result == 'SYSTEM_ERROR':
            return 5
        if result == "OUTPUT_LIMIT_EXCEED":
            return 9
        if result == "PRESENTATION_ERROR":
            return 10


class Submission(ModelParent, db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"))
    code = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(10))

    result = db.Column(db.Integer, default=JudgementStatus.PENDING)
    runtime_time = db.Column(db.Float)
    runtime_memory = db.Column(db.Integer)
    error_info = db.Column(db.Text, nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.now)
