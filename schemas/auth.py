# encoding:utf-8

login_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}

register_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string'},
    },
    'required': ['username', 'password', 'email']
}