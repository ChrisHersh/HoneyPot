from peewee import *

db = SqliteDatabase("data.db")

class BaseMode(Model):
    class Meta:
        database = db

class Password(BaseMode):
    password = CharField(unique=True)
    count = IntegerField()

class Username(BaseMode):
    username = CharField(unique=True)
    count = IntegerField()

class IPAddr(BaseMode):
    ip = CharField(unique=True)
    count = IntegerField()
