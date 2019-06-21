# encoding:utf-8
import uuid


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')