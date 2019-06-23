# encoding:utf-8
from utils import JsonSerializableMixin


class JudgementTask(JsonSerializableMixin):
    def __init__(self, task_id=None, problem_id=None, user_id=None, language=None, time_limit=None, memory_limit=None):
        self.id = task_id
        self.problem_id = problem_id
        self.user_id = user_id
        self.language = language
        self.time_limit = time_limit
        self.memory_limit = memory_limit


class JudgementResult(JsonSerializableMixin):
    def __init__(self, task_id=None, succeed=None, status=None, runtime_time=None, runtime_memory=None, error_info=None,
                 wrong_line= None, last_input=None, last_output=None, expected_output=None, timestamp=None):
        self.id = task_id
        self.succeed = succeed
        self.status = status
        self.runtime_time = runtime_time
        self.runtime_memory = runtime_memory
        self.error_info = error_info

        self.wrong_line = wrong_line
        self.last_input = last_input
        self.last_output = last_output
        self.expected_output = expected_output
        self.timestamp = timestamp
