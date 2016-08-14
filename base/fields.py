from uuid import uuid4


class NoDefault(Exception):
    """ No Default """
    def __init__(self, fieldname):
        super(NoDefault, self).__init__('Required field "%s" has no default set' % fieldname)


########################################################################################################################


class Field(object):
    _count = 0

    def __new__(cls, *args, **kwargs):
        Field._count += 1
        # print('Field[%d].__new__(%s, %r, %r)' % (cls._count, cls.__name__, args, kwargs))
        obj = super(Field, cls).__new__(cls)
        obj._count = Field._count
        return obj

    def __init__(self, label, required=True, default=NoDefault):
        # print('%s[%d].__init__(label=%r, default=%r)' % (self.__class__.__name__, self._count, label, default))
        self.label = label
        self.required = required
        self.default = default

    def __repr__(self):
        return '<%s:%r>' % (self.__class__.__name__, self.label)


class CharField(Field):
    def __init__(self, label=None, max_length=NoDefault, **kwargs):
        Field.__init__(self, label, **kwargs)
        self.max_length = max_length

    def clean(self, data):
        try:
            return unicode(data)
        except:
            raise


class IntField(Field):
    def __init__(self, label=None, min=None, max=None, **kwargs):
        Field.__init__(self, label, **kwargs)
        self.min = min
        self.max = max

    def clean(self, data):
        try:
            return int(data)
        except:
            raise


class IDField(Field):
    def __init__(self):
        Field.__init__(self, label=None, default=lambda: uuid4())
        self.min = min
        self.max = max

    def clean(self, data):
        try:
            return str(data)
        except:
            raise


class FloatField(Field):
    def __init__(self, label=None, min=None, max=None, **kwargs):
        Field.__init__(self, label, **kwargs)
        self.min = min
        self.max = max

    def clean(self, data):
        try:
            return float(data)
        except:
            raise
