# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          os.pardir))
sys.path.insert(0, parent_dir)

import pytest
from duc import Duc

test_data = {
    'check': 0,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'identifier': '41472389'
}

missed_data_i = {
    'check': 0,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'identifier': '41472389',
    'additional': 'Missed item'
}

missed_data_o = {
    'is_checked': False,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'id': 41472389,
    'additional': 'Missed item'
}

wrong_data = {
    'check': 0,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'identifier': '414s72389'
}

transformed = {
    'is_checked': False,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'id': 41472389
}


schema = {
    'check': {
        'validator': {},
        'transform': {
            'name': 'is_checked',
            'type': 'boolean'
        }
    },

    'token': {
        'validator': {
            'type': 'string'
        },
        'transform': {}
    },

    'network': {},

    'type': {
        'validator': {
            'type': 'integer'
        }
    },

    'identifier': {
        'validator': {},
        'transform': {
            'name': 'id',
            'type': 'integer'
        }
    },

}


d = Duc(schema)


def test_validation():
    assert d.validate(data=test_data)


def test_transformation():
    assert d.transduce(data=test_data)


def test_duc_process():
    d = Duc(schema, test_data)
    assert d.validate()
    assert d.errors is None
    assert d.transduce()
    print(d.result)
    assert d.result == transformed


def test_missed():
    d = Duc(schema, missed_data_i)
    assert d.transduce(append_missed=True)
    assert d.result == missed_data_o


def test_missed_output():
    missed_data_o = {
        'is_checked': False,
        'token': 'thetoken213',
        'type': 23,
        'network': 'VK',
        'id': 41472389,
        'additional': 'Missed item',
    }
    missed_data_r = {
        'is_checked': False,
        'token': 'thetoken213',
        'type': 23,
        'network': 'VK',
        'id': 41472389,
    }
    d = Duc(schema, missed_data_i)
    assert d.transduce(append_out=True)
    print('out ', d.out)
    assert d.result == missed_data_r
    assert d.out == missed_data_o


def test_invalid_data():
    with pytest.raises(ValueError):
        d.transduce(data=wrong_data)


def test_wrong_schema():
    # WS - wrong schema
    ws1 = {
        'field': 'transform'
    }

    ws2 = {
        'field': {
            'transform': {},
            'validator': {},
            'another': 'field'
        }
    }

    ws3 = {
        'field': {
            'transform': {
                'name': 'nn',
                'type': 'tt',
                'apply': 'aa',
                'another': 'field'
            },
            'validator': {},
        }
    }

    ws4 = {
        'field': {
            'transform': None,  # if you don't transform then do not specify this key or pass empty dict if you want customize in future!
        }
    }

    with pytest.raises(ValueError):
        d = Duc(ws1)

    with pytest.raises(ValueError):
        d = Duc(ws2)

    with pytest.raises(ValueError):
        d = Duc(ws3)

    with pytest.raises(ValueError):
        d = Duc(ws4)