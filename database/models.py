from peewee import *
from config_data.config import DATA_BASE_PATH


db = SqliteDatabase(DATA_BASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Hotels(BaseModel):
    user_id = IntegerField()
    hotel_info = TextField()
