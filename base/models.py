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

        def fdel(self):
            del self._data[fieldname]
        super(FieldProp, self).__init__(fget=fget, fset=fset, fdel=fdel, doc='Field %s' % fieldname)


class Meta(type):
    def __new__(cls, name, bases, body):
        # print('Meta.__new__(%r, %r, %r, %r)' % (cls, name, bases, body))
        fields = []
        if '__datastore__' not in body:
            body['__datastore__'] = datastore = OrderedDict

        for k, v in list(body.items()):
            if issubclass(v.__class__, Field):
                fields.append((k, v))
                del body[k]

        fields.sort(key=lambda i: i[1]._count)
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
        for k, v in kwargs.items():
            self._data[k] = v

    @property
    def cleaned_data(self):
        data = OrderedDict()
        for k, v in self._fields.items():
            if k in self._data:
                data[k] = self._data[k]
            else:
                default = v.default
                if default is NoDefault:
                    if v.required:
                        raise NoDefault(k)

                    default = None
                self._data[k] = data[k] = default() if callable(default) else default
        return data




