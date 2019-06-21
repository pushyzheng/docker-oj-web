# encoding:utf-8
from app import queue, db
from app.judgement.models import JudgementResult
from app.submission.models import JudgementStatus, Submission

@queue(queue='go-docker-judger-callback')
def judge_callback(ch, method, props, body):
    data = str(body, encoding='utf-8')
    print(data)

    result = JudgementResult()
    result.from_json_string(data)

    submission = Submission.query.filter_by(id=result.id).first()
    if not submission:
        print('The submission not found.')
        return

    if not result.succeed:
        submission.result = JudgementStatus.SYSTEM_ERROR
        print('Task {} system error.'.format(result.id))
        return

    submission.result = JudgementStatus.get_status(result.result)
    submission.error_info = result.error_info

    db.session.add(submission)
    db.session.commit()

