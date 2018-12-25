import os
from secrets import token_urlsafe

import peewee
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL'))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Url(BaseModel):
    base_url = peewee.TextField(unique=True)
    short_url = peewee.TextField(unique=True)

    @classmethod
    def get_url(cls, url):
        return cls.get_or_none(base_url=url)

    @classmethod
    def get_base_by_short(cls, short):
        return cls.get_or_none(short_url=short)

    @classmethod
    def add_url(cls, url):
        return cls.get_url(url) or cls.create_short_url(url)

    @classmethod
    def create_short_url(cls, url):
        short = token_urlsafe(5)
        return cls.create(base_url=url, short_url=short)


db.create_tables([Url], safe=True)
