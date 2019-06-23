# encoding:utf-8
import uuid
import json
from flask import jsonify

def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


def sort_and_distinct(data_list):
    data_list = list(set(data_list))
    list.sort(data_list)
    return data_list


def success(data):
    resp = {
        'data': data,
        'message': None,
        'code': 200
    }
    return jsonify(resp)