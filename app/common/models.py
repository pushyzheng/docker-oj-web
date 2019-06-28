# encoding:utf-8


class RoleName:
    ADMIN = 'ADMIN'
    USER = 'USER'

    @classmethod
    def get_weight_by_name(cls, name):
        if name == cls.ADMIN:
            return 3
        elif name == cls.USER:
            return 1


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


    @classmethod
    def get_desc_CN(cls, status):
        if status == cls.ACCEPTED:
            return '通过'
        elif status == cls.WRONG_ANSWER:
            return '答案错误'
        elif status == cls.COMPILE_ERROR:
            return '编译错误'
        elif status == cls.RUNTIME_ERROR:
            return '运行时错误'
