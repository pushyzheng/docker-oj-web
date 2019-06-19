# encoding:utf-8
from app import queue
from app.models import *


@queue(queue='go-docker-judger-callback')
def judge_callback(ch, method, props, body):
    data = str(body, encoding='utf-8')

    result = JudgementResult()
    result.from_json_string(data)

    print(result)
