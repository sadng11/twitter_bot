from base import Base
from sqlalchemy import Column, String, Integer, Text, DateTime


class TweetToken(Base):
    __tablename__ = 'tweet_token'

    id = Column(Integer, primary_key=True)
    tw_user_id = Column(String(255))
    next_token = Column(String(255), nullable=True, default=None)
    prev_token = Column(String(255), nullable=True, default=None)

    def __init__(self, tw_user_id, next_token, prev_token):
        self.tw_user_id = tw_user_id
        self.next_token = next_token
        self.prev_token = prev_token


class ReplyToken(Base):
    __tablename__ = 'reply_token'

    id = Column(Integer, primary_key=True)
    tw_id = Column(String(255))
    thread_id = Column(String(255))
    next_token = Column(Text, nullable=True, default=None)

    def __init__(self, tw_id, thread_id, next_token):
        self.tw_id = tw_id
        self.thread_id = thread_id
        self.next_token = next_token
