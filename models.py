"""
Models
by: Adam Dybczak (RaTilicus)
"""


from base import models
from base.fields import CharField, IDField, IntField


class Person(models.Model):
    id = IDField()
    name = CharField('Name')
    desc = CharField('Description', required=False)
    age = IntField('Age', required=True)
    index = IntField('Index', default=0)
