from base import Base
from sqlalchemy import Column, String, Integer, Text, DateTime


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    tw_id = Column(String(255))
    tw_author_id = Column(String(255))
    tw_text = Column(Text)
    tw_date = Column(DateTime)
    views = Column(Integer, default=None, nullable=True)
    quote_count = Column(Integer, default=None, nullable=True)
    reply_count = Column(Integer, default=None, nullable=True)
    retweet_count = Column(Integer, default=None, nullable=True)

    def __init__(self, tw_id, tw_author_id, tw_text, tw_date, views, quote_count, reply_count, retweet_count):
        self.tw_id = tw_id
        self.tw_author_id = tw_author_id
        self.tw_text = tw_text
        self.tw_date = tw_date
        self.views = views
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
