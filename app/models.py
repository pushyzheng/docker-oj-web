# encoding:utf-8
from app import db
import time
import json


class JsonClass(object):

    def to_json_string(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)

    def from_json_string(self, json_string):
        data = json.loads(json_string)

        for key in self.__dict__.keys():
            if key in data:
                setattr(self, key, data[key])

    def __str__(self):
        return str(self.__dict__)


class JudgementTask(JsonClass):
    def __init__(self, task_id=None, problem_id=None, user_id=None, language=None):
        self.id = task_id
        self.problem_id = problem_id
        self.user_id = user_id
        self.language = language


class JudgementResult(JsonClass):
    def __init__(self, task_id=None, succeed=None, result=None, duration=None, memory=None, error_info=None,
                 timestamp=None):
        self.id = task_id
        self.succeed = succeed
        self.result = result
        self.duration = duration
        self.memory = memory
        self.error_info = error_info
        self.timestamp = timestamp
