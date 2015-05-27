# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          os.pardir))
sys.path.insert(0, parent_dir)

import collections
import pytest
from duc import DottedList


def test_list_creation():
    empty_arr = DottedList()
    arr = DottedList([1, 2, 3, 4])
    assert isinstance(arr, DottedList)
    assert isinstance(arr, collections.Sequence)
    assert isinstance(arr, collections.Iterable)
    assert isinstance(arr, collections.MutableSequence)


def test_attr_access():
    arr = DottedList([1, 2, 3, 4])
    assert arr.e0 == 1
    assert arr.e3 == 4
    with pytest.raises(IndexError):
        out_range = arr.e4


def test_nested_list():
    arr_parent = [1, 2]
    arr_child = [3, 4]
    arr_parent.append(arr_child)
    arr = DottedList(arr_parent)
    assert arr.e2.e0 == 3
    assert arr.e2.e1 == 4


def test_nested_dict():
    arr_parent = [1, {'k': 2}]
    arr = DottedList(arr_parent)
    assert arr.e0 == 1
    assert arr.e1.k == 2


def test_nested_levels():
    arr_parent = [
        {
            'k': 2
        },
        {
            'v': [5, 6, 7, 8],
            'l': [9, {'i': 'very nested'}]
        }
    ]

    arr = DottedList(arr_parent)
    assert arr.e0.k == 2
    assert arr.e1.v.e0 == 5
    assert arr.e1.v.e3 == 8
    assert arr.e1.l.e0 == 9
    assert arr.e1.l.e1.i == 'very nested'


def test_nested_attributes():
    arr = DottedList([1])
    arr.e0 = [3, 5, [2, 9]]
    assert arr.e0.e0 == 3
    assert arr.e0.e2.e0 == 2
    assert arr.e0.e2.e1 == 9

if __name__ == '__main__':
    arr = DottedList([1, [5, 7]])
    print(type(arr.e1))
    arr.e0 = [3, 5, 7]
