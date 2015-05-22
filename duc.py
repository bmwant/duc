# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import logging
from collections import UserDict
from cerberus import Validator

logging.basicConfig(level=logging.DEBUG)

# todo: Add correct value validation for schema objects: check for existence of ('transform', 'validate',) and no other root key


class DottedDict(UserDict):
    """
    Dotted dictionary provides accessing dictionary items by dot-style attribute accessing
    """
    def __init__(self, data=None):
        if 'data' not in self.__dict__:
            self.__dict__['data'] = {}

        if data is not None:
            super(DottedDict, self).__init__(data)

    def __getattr__(self, key):
        try:
            return self.data[key]
        except KeyError as e:
            raise AttributeError(key)

    def __setitem__(self, name, value):
        self.data[name] = value

    def __setattr__(self, key, value):
        if 'data' not in self.__dict__:
            self.__dict__['data'] = {}
        self.__dict__['data'][key] = value
        super(DottedDict, self).__setattr__(key, value)


class Duc(object):
    def __init__(self, transduce_schema, data=None):
        self._schema = transduce_schema
        self._data = DottedDict()
        if data is not None:
            self._data.update(data)
        self._result = None
        self._errors = None
        self._transduced = False
        self._out = set()

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
                    self._out.add(name)
                else:
                    to_transform = False
            else:
                to_transform = False

            if not to_transform:
                logging.debug('No need to transform %s' % field)
                result[field] = data[field]

        # Append elements that are not listed in schema
        if append_missed:
            for field, value in data.items():
                try:
                    new_field_name = self._schema[field]['transform']['name']
                except KeyError:
                    new_field_name = field
                result[new_field_name] = value

                if field not in self._schema:
                    self._out.add(new_field_name)

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
            # todo: add implementation
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