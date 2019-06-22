from peewee import *
import datetime

db = SqliteDatabase("data.sqlite3")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    email = TextField(unique=True, index=True)
    password = TextField()

class Publication(BaseModel):
    title = CharField(index=True)
    body = TextField()
    creation_date = DateTimeField(default=datetime.datetime.now)
    update_date = DateTimeField(default=datetime.datetime.now)
    author = ForeignKeyField(User, backref="publications")

def create_tables():
    with db:
        db.create_tables([User, Publication, ])

def drop_tables():
    with db:
        db.drop_tables([User, Publication, ])