# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import logging
from collections import UserDict, UserList
from cerberus import Validator

logging.basicConfig(level=logging.DEBUG)


class DottedList(UserList):
    """
    Dotted list allows to use dot-notation when accessing list items by index: e.g.
    arr = ['a', 'b', 'c']
    arr[0] -> 'a'
    arr.e1 -> 'b'
    arr.e2 = 'd'
    arr[2] -> 'd'
    """
    def __init__(self, arr=None):
        if arr is not None and isinstance(arr, list):
            super().__init__()
            for elem in arr:
                if isinstance(elem, list):
                    self.data.append(DottedList(elem))
                elif isinstance(elem, dict):
                    self.data.append(DottedDict(elem))
                else:
                    self.data.append(elem)
        else:
            super().__init__(arr)

    def __getattr__(self, key):
        e = key[0]
        index = None
        try:
            index = int(key[1:])
        except ValueError:
            pass
        if e == 'e' and isinstance(index, int):
            return self.data[index]

        super().__getattribute__(key)

    def __setattr__(self, key, value):
        e = key[0]
        index = None
        try:
            index = int(key[1:])
        except ValueError:
            pass

        if e == 'e' and isinstance(index, int):
            if isinstance(value, list):
                self.data[index] = DottedList(value)
            else:
                self.data[index] = value
        else:
            super().__setattr__(key, value)


class DottedDict(UserDict):
    """
    Dotted dictionary provides accessing dictionary items by dot-style attribute accessing
    """
    def __init__(self, data=None):
        if data is not None and isinstance(data, dict):
            super().__init__()
            #self.__dict__['data'] = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    self.data[key] = DottedDict(value)
                elif isinstance(value, list):
                    self.data[key] = DottedList(value)
                else:
                    self.data[key] = value
        else:
            super().__init__(data)

    def __getattr__(self, key):
        try:
            return self.__dict__['data'][key]
        except KeyError as e:
            pass

        super().__getattribute__(key)

    def __setitem__(self, name, value):
        if isinstance(value, dict):
            self.__dict__['data'][name] = DottedDict(value)
        elif isinstance(value, list):
            self.__dict__['data'][name] = DottedList(value)
        else:
            self.__dict__['data'][name] = value

    def __setattr__(self, key, value):
        if 'data' in self.__dict__:
            self.__setitem__(key, value)
        else:
            super().__setattr__(key, value)

    def __delattr__(self, item):
        if item in self.data:
            del self.data[item]
        else:
            super().__delattr__(item)


class Duc(object):
    """
    Trans Duc er accepts some data, validate it if needed and make some transformations on it returning
    resulting data and output data to store somewhere
    """
    def __init__(self, transduce_schema, data=None):
        # Check if schema is correct
        valid_schema = self._check_schema(transduce_schema)
        if valid_schema:
            self._schema = transduce_schema
        else:
            raise ValueError('Invalid format of schema. Check documentation.')

        self._data = DottedDict()
        if data is not None:
            self._data.update(data)
        self._result = None
        self._errors = None
        self._transduced = False
        self._out = set()

    @staticmethod
    def _check_schema(schema):
        if not isinstance(schema, dict):
            return False

        for key, value in schema.items():
            allowed_params = ('transform', 'validator', )
            if not isinstance(value, dict):
                return False
            for param in value.keys():
                if param not in allowed_params:
                    return False

            allowed_transform = ('name', 'type', 'apply', 'out', )
            if 'transform' in value:
                operations = value['transform']
                if not isinstance(operations, dict):
                    return False
                for operation in operations:
                    if operation not in allowed_transform:
                        return False

            if 'validator' in value and not isinstance(value['validator'], dict):
                return False

            return True

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

    def transduce(self, data=None, append_missed=False, append_out=False):
        """
        You can also try to transduce unvalidated data
        :param data: Data to transform based on initial schema
        :param append_missed: append missed items that are not listed in shema to resulting data
        :param append_out: append missed items that are not listed in schema to output
        :return: True if transforming succeed
        """
        self._transduced = True
        result = DottedDict()

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
                    logging.info('Adding %s to out-data' % name)
                    self._out.add(name)
                else:
                    self._out.add(field)
                    to_transform = False
            else:
                self._out.add(field)
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

                if new_field_name not in result:
                    result[new_field_name] = value

        # Append elements that are not listed to the ouput
        if append_out:
            for field, value in data.items():
                if field not in self._schema:
                    self._out.add(field)

        if self._transduced:
            self._result = result
        else:
            self._result = None

        return self._transduced

    @staticmethod
    def cast_to_num(number):
        try:
            result = int(number)
        except ValueError:
            try:
                result = float(number)
            except ValueError:
                raise ValueError('Cannot parse a number from %s value' % number)
        return result

    @staticmethod
    def cast_to_datetime(date):
        from dateutil.parser import parse
        try:
            result = parse(date)
        except ValueError:
            ValueError('Cannot parse a date from %s value' % date)
        return result

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

            'datetime': self.cast_to_datetime,
            'number': self.cast_to_num
        }
        if cast_key in casters:
            return casters[cast_key]
        raise KeyError('No such caster to transduce your data: [%s]' % cast_key)


    @property
    def out(self):
        out = {}
        for elem in self._out:
            if elem in self._result:
                out[elem] = self._result[elem]
            else:
                out[elem] = self._data[elem]
        return out

    @property
    def result(self):
        return self._result

    @property
    def errors(self):
        return self._errors