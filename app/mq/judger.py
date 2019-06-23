# encoding:utf-8
from app import queue, db, app
from app.judgement.models import JudgementResult
from app.submission.models import JudgementStatus, Submission
from utils import logger
import os


@queue(queue='go-docker-judger-callback')
def judge_callback(ch, method, props, body):
    data = str(body, encoding='utf-8')
    logger.info(data)

    result = JudgementResult()
    result.from_json_string(data)

    submission = Submission.query.filter_by(id=result.id).first()
    if not submission:
        logger.error('The submission not found.')
        return

    if not result.succeed:
        logger.error('Task {} system error.'.format(result.id))
        submission.result = JudgementStatus.SYSTEM_ERROR
        submission.error_info = result.error_info
        return

    submission.result = JudgementStatus.get_status(result.status)
    submission.error_info = result.error_info
    submission.last_input = result.last_input
    submission.last_output = result.last_output
    submission.expected_output = result.expected_output
    submission.runtime_time = result.runtime_time
    submission.runtime_memory = result.runtime_memory

    submission.case_passing_rate = get_case_passing_rate(result.wrong_line, result.id)

    db.session.add(submission)
    db.session.commit()


# 计算该次提交样例的通过率
def get_case_passing_rate(wrong_line, problem_id):
    problem_case_path = '{}/case_{}.txt'.format(app.config['CASE_PATH'], problem_id)
    if not os.path.exists(problem_case_path):
        return -1

    with open(problem_case_path) as f:
        lines = f.readlines()
        return (wrong_line - 1) / (len(lines))
