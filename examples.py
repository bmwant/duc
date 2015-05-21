# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from duc import Duc

schema = {
    'num': {
        'transform': {
            'name': 'the_num',
            'type': 'integer',
            'out': False
        }
    },
    'to_db': {
        'transform': {
            'name': 'db_value',
            'type': 'string',
            'apply': str.upper,
        }
    }
}


def test_validation():
    local_data = {
        'num': '234'
    }
    local_schema = {
        'num': {
            'transform': {
                'name': 'the_num',
                'type': 'integer'
            }
        }
    }
    d = Duc(local_schema, local_data)
    if d.validate():
        if d.transduce():
            print(d.result)
    else:
        print('Input data is not valid')


def specify_out_data():
    local_data = {
        'num': '234',
        'to_db': 'lalka'
    }
    d = Duc(schema, local_data)
    if d.transduce():
        print(d.result)
        print(d.out)

def apply_some_func():
    pass


if __name__ == '__main__':
    test_validation()
    specify_out_data()