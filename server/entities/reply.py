from base import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean


class Reply(Base):
    __tablename__ = 'reply'

    id = Column(Integer, primary_key=True)
    reply_id = Column(String(255))
    author_id = Column(String(255))
    tw_ref_id = Column(String(255))
    text = Column(Text)
    blue_verified = Column(Boolean)
    location = Column(String(300))
    name = Column(String(300), nullable=True, default=None)
    screen_name = Column(String(300), nullable=True, default=None)
    followers_count = Column(Integer, nullable=True, default=None)
    friends_count = Column(Integer, nullable=True, default=None)
    views = Column(Integer, nullable=True, default=None)
    creat_date = Column(DateTime)

    def __init__(self, reply_id, author_id, tw_ref_id, text, blue_verified, location, name, screen_name,
                 followers_count, friends_count, views, creat_date):
        self.reply_id = reply_id
        self.author_id = author_id
        self.tw_ref_id = tw_ref_id
        self.text = text
        self.blue_verified = blue_verified
        self.location = location
        self.name = name
        self.screen_name = screen_name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.views = views
        self.creat_date = creat_date
