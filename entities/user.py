from flask_marshmallow import Schema
from sqlalchemy import Column, String, Integer
from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tw_username = Column(String(255))
    tw_name = Column(String(255))
    tw_uid = Column(String(255))

    def __init__(self, tw_username, tw_name, tw_uid):
        self.tw_username = tw_username
        self.tw_uid = tw_uid
        self.tw_name = tw_name


class UserSchema(Schema):
    class Meta:
        fields = ("id", "tw_username", "tw_name", "tw_uid")
        model = User
