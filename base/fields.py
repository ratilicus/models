"""
Models
by: Adam Dybczak (RaTilicus)
"""


from uuid import uuid4


class NoDefault(Exception):
    """ No Default """
    def __init__(self, fieldname=None):
        super(NoDefault, self).__init__('Required field "%s" has no default set' % fieldname)


class ValidationError(Exception):
    """ Field Validation """

########################################################################################################################


class Field(object):
    blank_value = None
    _instance_count = 0

    def __new__(cls, *args, **kwargs):
        obj = super(Field, cls).__new__(cls)
        obj._index = Field._instance_count
        Field._instance_count += 1
        return obj

    @staticmethod
    def get_instance_count():
        return Field._instance_count

    @property
    def index(self):
        return self._index

    @property
    def has_default(self):
        return self._default is not NoDefault

    @property
    def default(self):
        return self._default() if callable(self._default) else self._default

    def __init__(self, label=None, required=True, default=NoDefault):
        self.label = label
        self.required = required
        self._default = default

    def __repr__(self):
        return '<%s:%r>' % (self.__class__.__name__, self.label)


class IDField(Field):
    def __init__(self):
        Field.__init__(self, default=lambda: str(uuid4()))

    def clean(self, data):
        return str(data)


class CharField(Field):
    blank_value = u''

    def __init__(self, label=None, max_length=None, **kwargs):
        Field.__init__(self, label, **kwargs)
        self.max_length = max_length

    def clean(self, data):
        try:
            cleaned_data = unicode(data)

        except:
            raise

        if self.max_length > 0 and len(cleaned_data) > self.max_length:
            raise ValidationError('Value is longer than the maximum length')

        return cleaned_data


class IntField(Field):
    def __init__(self, label=None, min=None, max=None, **kwargs):
        Field.__init__(self, label, **kwargs)
        self.min = min
        self.max = max

    def clean(self, data):
        try:
            cleaned_data = int(data)

        except ValueError:
            raise ValidationError('Invalid field value')

        except:
            raise

        if self.min is not None and cleaned_data < self.min:
            raise ValidationError('Value is less than the minimum')

        if self.max is not None and cleaned_data > self.max:
            raise ValidationError('Value is greater than the maximum')

        return cleaned_data


class FloatField(Field):
    def __init__(self, label=None, min=None, max=None, **kwargs):
        Field.__init__(self, label, **kwargs)
        self.min = min
        self.max = max

    def clean(self, data):
        try:
            cleaned_data = float(data)

        except ValueError:
            raise ValidationError('Invalid field value')

        except:
            raise

        if self.min is not None and cleaned_data < self.min:
            raise ValidationError('Value is less than the minimum')

        if self.max is not None and cleaned_data > self.max:
            raise ValidationError('Value is greater than the maximum')

        return cleaned_data
