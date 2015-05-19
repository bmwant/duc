# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from duc import Duc

data = {
    'num': '234'
}

schema = {
    'num': {
        'transform': {
            'name': 'the_num',
            'type': 'integer'
        }
    }
}


def test_validation():
    d = Duc(schema, data)
    if d.validate():
        if d.transduce():
            print(d.result)
    else:
        print('Input data is not valid')


if __name__ == '__main__':
    test_validation()