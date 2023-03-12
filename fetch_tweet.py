import argparse
import datetime as fdatetime
import os
import traceback
from datetime import datetime
from time import sleep
import tzlocal
from base import Session, Base, engine
from entities.process import Process
from entities.tokens import TweetToken
from entities.tweet import Tweet
from fetch_comments import FetchComments
from tweet import Tweeter
from decouple import config

if config('PROXY', default=False, cast=bool):
    os.environ['http_proxy'] = 'http://127.0.0.1:8889'
    os.environ['https_proxy'] = 'http://127.0.0.1:8889'

parser = argparse.ArgumentParser()
parser.add_argument('--user_id', required=True)
args = parser.parse_args()

Base.metadata.create_all(engine)
session = Session()

th_list = []
next_token = None
flag = True
process_list_count = 5
tweet = Tweeter()
while flag:
    try:
        process_list = session.query(Process).filter(Process.tw_user_id == args.user_id).count()
        if process_list <= 0:
            tw_dict = {
                "start_time": fdatetime.datetime(2023, 2, 1, 00, 00, 00),
                "user_id": args.user_id
            }
            user_token_paginate = session.query(TweetToken).filter(TweetToken.tw_user_id == args.user_id).one_or_none()
            if next_token is None and user_token_paginate is not None:
                if user_token_paginate.prev_token is not None:
                    tw_dict.update({"pagination_token": user_token_paginate.prev_token})
            if next_token is not None:
                tw_dict.update({"pagination_token": next_token})
            sleep(3)
            json_data = tweet.get_tweets(**tw_dict)
            local_timezone = tzlocal.get_localzone()

            if json_data['data'] is not None:
                for item in json_data['data']:
                    tweet_data = item['legacy']
                    process = Process(str(os.getpid()), datetime.now(), args.user_id)
                    session.add(process)
                    session.commit()
                    if session.query(Tweet).filter(Tweet.tw_id == tweet_data['id_str']).one_or_none() is None:
                        s = item['legacy']['created_at'].split(' ')
                        date = "{} {} {} {}".format(s[0], s[2], s[1], s[5])
                        time = s[3]
                        datetime_object = datetime.strptime("{} {}".format(date, time), '%a %d %b %Y %H:%M:%S')
                        session.add(Tweet(tweet_data['id_str'], tweet_data['user_id_str'], tweet_data['full_text'],
                                          datetime_object, int(item['views']['count']), tweet_data['quote_count'],
                                          tweet_data['reply_count'], tweet_data['retweet_count']))
                        session.commit()
                        # print('insert tweet')

                    th_list.append(
                        {'thread': FetchComments(tweet_id=tweet_data['id_str']),
                         'db_id': process.id})
                    th_list[len(th_list) - 1]['thread'].start()
                    # sleep(3600)
                if 'next_token' in json_data['meta']:
                    nex_token = None
                    prev_token = None
                    if 'next_token' in json_data['meta']:
                        nex_token = json_data['meta']['next_token']
                    session.query(TweetToken).filter(TweetToken.tw_user_id == args.user_id).delete()
                    session.add(TweetToken(args.user_id, next_token, None))
                    session.commit()
                    next_token = json_data['meta']['next_token']
                    # print("get next token")

                for x in th_list:
                    x['thread'].join()
                    session.query(Process).filter(Process.id == x['db_id']).delete()
                    session.commit()
            else:
                # print("error in fetch tweet.detail is : {}".format(json_data['detail']))
                if json_data['detail'] == 'Rate limit exceeded':
                    sleep(30)
        else:
            sleep(5)
    except Exception as e:
        # print("error in fetch tweet")
        # print(e)
        # print(traceback.format_exc())
        flag = True
        sleep(2)
