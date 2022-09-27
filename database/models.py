from peewee import *
from config_data.config import DATA_BASE_PATH


db = SqliteDatabase(DATA_BASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    name = CharField()
    user_id = IntegerField()


class Hotels(BaseModel):
    user_id = IntegerField()
    hotel_info = TextField()


def create_tables():
    Users.create_table()
    Hotels.create_table()
