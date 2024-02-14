from peewee import *

db = SqliteDatabase("dream.db")


class Dream(Model):
    rating = SmallIntegerField()
    desc = CharField()
    date = DateField()

    class Meta:
        database = db
