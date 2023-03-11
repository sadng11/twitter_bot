from base import Base
from sqlalchemy import Column, String, Integer, Text, DateTime


class Process(Base):
    __tablename__ = 'process'

    id = Column(Integer, primary_key=True)
    pid = Column(String(255))
    date = Column(DateTime)
    tw_user_id = Column(String(255))

    def __init__(self, pid, date, tw_user_id):
        self.pid = pid
        self.tw_user_id = tw_user_id
        self.date = date
