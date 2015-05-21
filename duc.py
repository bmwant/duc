# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import logging
from cerberus import Validator

logging.basicConfig(level=logging.DEBUG)


class Duc(object):
    def __init__(self, transduce_schema, data=None):
        self._schema = transduce_schema
        self._data = data
        self._result = None
        self._errors = None
        self._transduced = False
        self._out = []

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

    def transduce(self, data=None, append_missed=False):
        """
        You can also try to transduce unvalidated data
        :param data:
        :param append_missed:
        :return:
        """
        self._transduced = True
        result = {}

        if data is None:
            data = self._data

        for field, value in self._schema.items():
            if field not in data:
                raise ValueError('Input data does not corresponds to schema provided. No such key: %s' % field)

            to_transform = True
            if value:
                if 'transform' in value and value['transform']:
                    transform_data = value['transform']

                    name = field
                    if 'name' in transform_data and isinstance(transform_data['name'], str):
                        name = transform_data['name']

                    if 'type' in transform_data:
                        caster = self._get_cast(transform_data['type'])
                        to_cast = data[field]
                        try:
                            result[name] = caster(to_cast)
                        except ValueError as e:
                            self._transduced = False
                            raise ValueError('Cannot cast {}: {} with built-in {}'.format(name, to_cast, caster))
                    else:
                        result[name] = data[field]

                    if 'apply' in transform_data and hasattr(transform_data['apply'], '__call__'):
                        result[name] = transform_data['apply'](result[name])

                    if 'out' in transform_data and transform_data['out'] == False:
                        continue
                    self._out.append(name)
                else:
                    to_transform = False
            else:
                to_transform = False

            if not to_transform:
                logging.debug('No need to transform %s' % field)
                result[field] = data[field]

        if append_missed:
            for field, value in data.items():
                try:
                    new_field_name = self._schema[field]['transform']['name']
                except KeyError:
                    result[field] = value


        if self._transduced:
            self._result = result
        else:
            self._result = None

        return self._transduced

    def _get_cast(self, cast_key: str) -> type:

        def not_impl(obj):
            raise NotImplementedError('Still implementing')

        casters = {
            'string': str,
            'integer': int,
            'float': float,
            'boolean': bool,
            'dict': dict,
            'list': list,
            'set': set,

            'object': not_impl,
            'datetime': not_impl,
            'number': not_impl
        }
        if cast_key in casters:
            return casters[cast_key]
        raise KeyError('No such caster to transduce your data: [%s]' % cast_key)


    @property
    def out(self):
        out = {}
        for elem, value in self._result.items():
            if elem in self._out:
                out[elem] = value
        return out

    @property
    def result(self):
        return self._result

    @property
    def errors(self):
        return self._errors