# encoding:utf-8
from app.models import JsonSerializableMixin


class JudgementTask(JsonSerializableMixin):
    def __init__(self, task_id=None, problem_id=None, user_id=None, language=None, time_limit=None, memory_limit=None):
        self.id = task_id
        self.problem_id = problem_id
        self.user_id = user_id
        self.language = language
        self.time_limit = time_limit
        self.memory_limit = memory_limit


class JudgementResult(JsonSerializableMixin):
    def __init__(self, task_id=None, succeed=None, result=None, duration=None, memory=None, error_info=None,
                 timestamp=None):
        self.id = task_id
        self.succeed = succeed
        self.result = result
        self.duration = duration
        self.memory = memory
        self.error_info = error_info
        self.timestamp = timestamp
