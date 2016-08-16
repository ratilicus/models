"""
Models
by: Adam Dybczak (RaTilicus)
"""


from collections import OrderedDict
from inspect import isclass
from fields import (NoDefault, Field)


class FieldProp(property):
    def __init__(self, fieldname, field):
        def fget(self):
            if fieldname in self._data:
                val = self._data[fieldname]
            else:
                val = None
            return val

        def fset(self, value):
            self._data[fieldname] = value
            self._dirty_fields.add(fieldname)

        def fdel(self):
            del self._data[fieldname]
            self._dirty_fields.add(fieldname)

        super(FieldProp, self).__init__(fget=fget, fset=fset, fdel=fdel, doc='Field %s' % fieldname)


class Meta(type):
    def __new__(cls, name, bases, body):
        # print('Meta.__new__(%r, %r, %r, %r)' % (cls, name, bases, body))
        fields = []
        for k, v in list(body.items()):
            if issubclass(v.__class__, Field):
                fields.append((k, v))
                del body[k]

        fields.sort(key=lambda i: i[1].index)
        for k, v in fields:
            body[k] = FieldProp(k, v)

        body['_fields'] = OrderedDict(fields)
        obj = type.__new__(cls, name, bases, body)
        return obj


class Model(object):
    __metaclass__ = Meta
    __datastore__ = OrderedDict

    def __init__(self, **kwargs):
        self._data = self.__datastore__() if isclass(self.__datastore__) else self.__datastore__
        self._dirty_fields = set(self._fields)
        self._clean_data = OrderedDict()
        self._errors = []
        for fieldname, value in kwargs.items():
            self._data[fieldname] = value

    def is_valid(self):
        errors = self._errors
        del errors[:]
        data = self._clean_data
        for fieldname in self._dirty_fields:
            if fieldname in self._data:
                value = self._data[fieldname]

            else:
                field = self._fields[fieldname]
                if field.has_default:
                    value = field.default

                else:
                    if field.required:
                        raise NoDefault(fieldname)

                    value = field.blank_value

            data[fieldname] = field.clean(value)

        self._dirty_fields.clear()
        return data

    @property
    def cleaned_data(self):
        return None if self._dirty_fields else self._clean_data




