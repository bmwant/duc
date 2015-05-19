# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from cerberus import Validator


class Duc(object):
    def __init__(self, transduce_schema, data=None):
        self._schema = transduce_schema
        self._data = data
        self._result = None
        self._errors = None

    def validate(self, data=None):
        validation_schema = {}
        for field, value in self._schema.items():
            if value is not None and 'validator' in value:
                validation_schema[field] = value['validator']

        validator = Validator(validation_schema, allow_unknown=True)

        if data is None:
            result = validator.validate(self._data)
        else:
            result = validator.validate(data)

        if not result:
            self._errors = validator.errors

        return result

    def transduce(self, data=None):
        result = {}

        if data is None:
            data = self._data

        for field, value in self._schema.items():
            if value is not None and 'transform' in value:
                transform_data = value['transform']
                if transform_data is None:
                    result[field] = data[field]
                    continue

                name = field
                if 'name' in transform_data and isinstance(transform_data['name'], str):
                    name = transform_data['name']

                if 'type' in transform_data:
                    try:
                        result[name] = self._get_cast(transform_data['type'])(data[field])
                    except Exception as e:
                        raise e
                else:
                    result[name] = data[field]

        self._result = result
        return True

    def _get_cast(self, cast_key: str) -> type:
        casters = {
            'string': str,
            'integer': int,
            'float': float,
            'boolean': bool,
            'dict': dict,
            'list': list,
            'set': set,

            'object': '',
            'datetime': '',
            'number': ''
        }
        if cast_key in casters:
            return casters[cast_key]
        raise KeyError('No such caster to transduce your data: [%s]' % cast_key)

    @property
    def result(self):
        return self._result

    @property
    def errors(self):
        return self._errors