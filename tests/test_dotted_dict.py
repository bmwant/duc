# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'

import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          os.pardir))
sys.path.insert(0, parent_dir)

import collections
import pytest
from duc import DottedDict


def test_dict_creation():
    dct = DottedDict({'k': 1, 'v': 2})
    assert isinstance(dct, DottedDict)
    assert isinstance(dct, collections.Mapping)
    assert isinstance(dct, collections.MutableMapping)
    assert isinstance(dct, collections.Iterable)


def test_attr_access():
    dct = DottedDict({'k': 1, 'v': 2})
    assert dct.k == 1
    assert dct.v == 2
    dct.k = 3
    dct.v = 4
    assert dct.k == 3
    assert dct.v == 4
    dct.t = 'new value'
    assert dct.t == 'new value'


def test_attr_remove():
    dct = DottedDict({'k': 1, 'v': 2})
    del dct.k
    with pytest.raises(AttributeError):
        p = dct.k

    dct.k = 'new value'
    assert dct.k == 'new value'
    assert dct.v == 2


def test_nested_dict():
    nst_dct = {
        'k': {
            'i': 1,
            'j': 2,
        },
        'v': {
            'l': 4,
            'm': 5,
        }
    }

    dct = DottedDict(nst_dct)
    assert dct.k.i == 1
    assert dct.k.j == 2
    assert dct.v.l == 4
    assert dct.v.m == 5


def test_nested_list():
    dct = DottedDict({
        'k': [1, 2, 3]
    })
    assert dct.k.e0 == 1
    assert dct.k.e1 == 2
    assert dct.k.e2 == 3
    assert dct.k == [1, 2, 3]


def test_nested_levels():
    dct = DottedDict({
        'k': [2,
            {
                'v': [7, 8, 9]
            }]
    })

    assert dct.k.e0 == 2
    assert dct.k.e1.v == [7, 8, 9]
    assert dct.k.e1.v.e2 == 9


if __name__ == '__main__':
    dct = DottedDict({'key1': 'value1', 'key2': 'value2'})
    print(dct)
    print(dct.keys())
    print(dct.values())
    print(dct.items())