# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import pytest
from duc import Duc

test_data = {
    'check': 0,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'identifier': '41472389'
}

missed_data = {
    'check': 0,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'identifier': '41472389',
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

missed_trans = {
    'is_checked': False,
    'token': 'thetoken213',
    'type': 23,
    'network': 'VK',
    'id': 41472389,
    'additional': 'Missed item'
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

invalid_schema = {

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
    d = Duc(schema, missed_data)
    assert d.transduce(append_missed=True)
    print(d.result)
    assert d.result == missed_trans


def test_invalid_schema():
    with pytest.raises(ValueError):
        d.transduce(data=wrong_data)