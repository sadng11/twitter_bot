import os
import subprocess
import tweepy
from base import Session, Base, engine
from decouple import config
import requests

from entities.user import User


if config('PROXY', default=False, cast=bool):
    os.environ['http_proxy'] = 'http://127.0.0.1:8889'
    os.environ['https_proxy'] = 'http://127.0.0.1:8889'

Base.metadata.create_all(engine)
session = Session()

process_list_count = 3

while True:
    username = input("Enter username: ")

    flag = True

    client = tweepy.Client(
        bearer_token=config('BEARER_TOKEN'),
        consumer_key=config('CONSUMER_KEY'),
        consumer_secret=config('CONSUMER_SECRET'),
        access_token=config('ACCESS_TOKEN'),
        access_token_secret=config('ACCESS_TOKEN_SECRET'),
        return_type=requests.Response,
        wait_on_rate_limit=True)

    try:
        user_data_res = client.get_user(username=username)
        user_data = user_data_res.json()['data']
        if session.query(User).filter(User.tw_uid == user_data['id']).one_or_none() is None:
            session.add(User(user_data['username'], user_data['name'], user_data['id']))
            session.commit()
        subprocess.Popen(
            ["python", 'fetch_tweet.py', '--user_id', user_data['id']])
    except Exception as e:
        print(e)
        exit()
