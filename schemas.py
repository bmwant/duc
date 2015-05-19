# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from duc import Duc

user_data = {
    'first': False,
    'token': 'test',
    'gender': 2,
    'network': 'VK',
    'bYear': '1994',
    'group': 'A',
    'uid': '414s72389'
}

user_data_schema = {
    'first': {
        'validator': {
            'type': 'boolean'
        },
        'transform': {
            'name': 'first_time',
            'type': 'boolean'
        }
    },
    'token': None,
    'gender': {
        'validator': {
            'type': 'integer'
        }
    },
    'bYear': {
        'transform': None
    },
    'uid': {
        'validator': {
            'type': 'string'
        },
        'transform': {
            'name': 'user_id',
            'type': 'integer'
        }
    },
}

d = Duc(user_data_schema)
print(d.validate(user_data))
print(d.errors)
print(d.transduce(user_data))
print(d.result)
