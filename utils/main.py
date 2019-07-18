# encoding:utf-8
import uuid
import json
from datetime import datetime
from flask import jsonify

def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


def sort_and_distinct(data_list):
    data_list = list(set(data_list))
    list.sort(data_list)
    return data_list


def get_day_zero_time(date):
    result = datetime.now().replace(year=date.year, month=date.month,
                                    day=date.day, hour=0, minute=0, second=0)
    return result


def success(data=None):
    resp = {
        'data': data,
        'message': None,
        'code': 200
    }
    return jsonify(resp)