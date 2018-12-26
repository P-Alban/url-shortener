import os

import peewee
from playhouse.db_url import connect

import utils

db = connect(os.environ.get('DATABASE_URL'))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Url(BaseModel):
    base_url = peewee.TextField(unique=True)

    @classmethod
    def get_url(cls, url):
        return cls.get_or_none(base_url=url)

    @classmethod
    def get_base_by_short(cls, short):
        return cls.get_or_none(id=utils.decode(short))

    @classmethod
    def add_url(cls, url):
        return cls.get_url(url) or cls.create(base_url=url)


db.create_tables([Url], safe=True)
