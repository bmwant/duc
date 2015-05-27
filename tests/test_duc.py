# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          os.pardir))
sys.path.insert(0, parent_dir)

import datetime
import pytest
from duc import Duc, DottedDict

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


def test_result_type():
    minus_32 = lambda x: x-32
    schema = {
        'id': {
            'transform': {
                'name': 'user_id',
                'type': 'string',
                'apply': str.upper
            }
        },

        'inc_age': {
            'transform': {
                'name': 'age',
                'type': 'integer',
                'apply': minus_32,
                'out': False
            }
        }

    }

    data_input = {
        'id': 'user555666',
        'inc_age': '45'
    }

    data_output = {
        'user_id': 'USER555666'
    }

    data_result = {
        'user_id': 'USER555666',
        'age': 13
    }

    d = Duc(schema, data_input)
    d.transduce()
    assert d.result == data_result
    assert d.out == data_output
    assert isinstance(d.result, DottedDict)
    assert d.result.user_id == 'USER555666'
    assert d.result.age == 13


def test_date_transforming():
    schema = {
        'created': {
            'transform': {
                'name': 'date_created',
                'type': 'datetime'
            }
        }
    }

    data_input = {
        'created': '09-27-1996',
    }

    d = Duc(schema)
    d.transduce(data=data_input)
    assert d.result['date_created'].year == 1996
    assert isinstance(d.result.date_created, datetime.datetime)

if __name__ == '__main__':
    pass