# encoding:utf-8

save_problem_schema = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'content': {'type': 'string'},
        'time_limit': {'type': 'integer'},
        'memory_limit': {'type': 'integer'},
        'case_list': {'type': 'array'},
        'answer_list': {'type': 'array'}
    },
    'required': ['title', 'content', 'time_limit', 'memory_limit', 'case_list', 'answer_list']
}

update_problem_schema = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'content': {'type': 'string'},
        'time_limit': {'type': 'integer'},
        'memory_limit': {'type': 'integer'}
    },
    'required': []
}

update_cases_answers_schema = {
    'type': 'object',
    'properties': {
        'case_list': {'type': 'array'},
        'answer_list': {'type': 'array'}
    },
    'required': ['case_list', 'answer_list']
}
