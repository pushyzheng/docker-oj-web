# encoding:utf-8
from app import db
from utils import ModelParent


class Label(db.Model, ModelParent):
    __tablename__ = 'labels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(36))

    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
