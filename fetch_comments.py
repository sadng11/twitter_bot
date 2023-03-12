import os
import random
from datetime import datetime
from threading import Thread
from time import sleep
from base import Session
from entities.reply import Reply
from entities.tokens import ReplyToken
from sqlalchemy import desc
from decouple import config
import sentry_sdk
from tweet import Tweeter

if config('PROXY', default=False, cast=bool):
    os.environ['http_proxy'] = 'http://127.0.0.1:8889'
    os.environ['https_proxy'] = 'http://127.0.0.1:8889'


class FetchComments(Thread):
    def __init__(self, tweet_id):
        super().__init__()
        self.tweet_id = tweet_id

    def run(self):
        flag = True
        next_token_reply = None
        session = Session()

        sentry_sdk.init(
            dsn=config("SENTRY_URL"),
            traces_sample_rate=1.0
        )
        while flag:
            try:
                q_f = {'tweet_id': self.tweet_id}
                token_paginate = session.query(ReplyToken).filter(
                    ReplyToken.tw_id == self.tweet_id).order_by(desc("id")).limit(2).all()
                if next_token_reply is None and len(token_paginate) > 0:
                    if len(token_paginate) == 2:
                        q_f.update({"next_token": token_paginate[1].next_token})
                if next_token_reply is not None:
                    q_f.update({"next_token": next_token_reply})

                sleep(random.randint(3, 5))
                # print("fetching reply in {}".format(self.name))

                reply_res_json = Tweeter().get_reply(**q_f)
                if reply_res_json['data'] is not None:
                    for item in reply_res_json['data']:
                        reply_data = item['legacy']
                        views = None
                        if 'count' in item['views']:
                            views = int(item['views']['count'])
                        if session.query(Reply).filter(
                                Reply.reply_id == reply_data['conversation_id_str']).one_or_none() is None:
                            s = reply_data['created_at'].split(' ')
                            date = "{} {} {} {}".format(s[0], s[2], s[1], s[5])
                            time = s[3]
                            datetime_object = datetime.strptime("{} {}".format(date, time), '%a %d %b %Y %H:%M:%S')
                            ref_id = reply_data['conversation_id_str']
                            core_item = item['core']['user_results']['result']
                            session.add(
                                Reply(reply_data['id_str'], reply_data['user_id_str'], ref_id, reply_data['full_text'],
                                      core_item['is_blue_verified'],
                                      core_item['legacy']['location'], core_item['legacy']['name'],
                                      core_item['legacy']['screen_name'], core_item['legacy']['followers_count'],
                                      core_item['legacy']['friends_count'], views,
                                      datetime_object))
                            session.commit()
                            # print("insert reply in {}".format(self.name))
                    if 'meta' in reply_res_json and 'next_token' in reply_res_json['meta']:
                        next_token_reply = reply_res_json['meta']['next_token']
                        session.add(ReplyToken(self.tweet_id, self.name, next_token_reply))
                        session.commit()
                    else:
                        flag = False
                else:
                    # print("error in fetch tweet.detail is : {}".format(reply_res_json['detail']))
                    if reply_res_json['detail'] == 'Rate limit exceeded':
                        sleep(30)
                    flag = False
            except Exception as e:
                # print("error in reply with tw_id : {} ,thread : {}".format(self.tweet_id, self.name))
                # print(traceback.format_exc())
                # print(e)
                sleep(2)
