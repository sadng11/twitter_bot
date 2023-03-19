import json
from datetime import datetime
import urllib.parse

import requests

from obj import json_vars


class Tweeter:
    def __init__(self):
        self.__set_session()
        self.response = None
        self.result = None
        self.base_url = 'https://api.twitter.com'

    def __headers(self):
        return {
            'authorization': "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            'content-type': 'application/json',
            'x-csrf-token': '78d4683d9b207b701d63ac4b7d368c0f4c1e08f55decdbf24cb343dd5773829fe33f516bea9c1132a593493c6fb9eff419b105ceeb393e2b9825947d97d3e398c081d65e12b92b421a55942f217a97df',
            'x-twitter-auth-type': "OAuth2Session",
            "x-twitter-active-user": "yes",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "origin": "https://twitter.com",
            "referer": "https://twitter.com",
            "cookie": 'guest_id=v1%3A167794875275568252; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCKwkiq2GAToMY3NyZl9p%250AZCIlNWM3OGI5NDExYzExYTJhNzY5ZjRiN2MxY2RhYzhjMmI6B2lkIiVjOTI2%250AODUxZWY0MjUzYmM0NWQ4MTZhNDkxMWJlN2FjYw%253D%253D--aa1aaf4ef00d00a56193fd1564e94ba07ff9ef39; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A167794875275568252; guest_id_marketing=v1%3A167794875275568252; personalization_id="v1_jDFRXINeCSAKnbTaOxBOGA=="; at_check=true; eu_cn=1; des_opt_in=Y; _gcl_au=1.1.1967108419.1677948937; kdt=gX5YztpygNkndQyXnqaMTLGqEzu2Aloyo7jDjoyN; auth_token=472b6345b054b14e103124a08ce014c63d6dcecf; ct0=78d4683d9b207b701d63ac4b7d368c0f4c1e08f55decdbf24cb343dd5773829fe33f516bea9c1132a593493c6fb9eff419b105ceeb393e2b9825947d97d3e398c081d65e12b92b421a55942f217a97df; twid=u%3D1581327752514371584; lang=en; _gid=GA1.2.884642797.1678292420; external_referer=padhuUp37zixoA2Yz6IlsoQTSjz5FgRcKMoWWYN3PEQ%3D|0|8e8t2xd8A2w%3D; mbox=PC#0d0604f9dd9d41bab0dd2613afd8f0ee.37_0#1741608468|session#81cc86b6f91b42f59f0f331df89de490#1678365528; _ga_34PHSZMC42=GS1.1.1678362876.7.1.1678363680.0.0.0; _ga=GA1.2.713842151.1677948865'
        }

    def __set_session(self):
        self.session = requests.session()

    def get_reply(self, **kwargs):
        if 'next_token' in kwargs:
            json_vars['reply_vars'].update({"cursor": kwargs['next_token']})
        if 'tweet_id' in kwargs:
            json_vars['reply_vars'].update({"focalTweetId": kwargs['tweet_id']})
        str_vars = 'variables={}&features={}'.format(
            urllib.parse.quote(json.dumps(json_vars['reply_vars']).replace(' ', '')),
            urllib.parse.quote(json.dumps(json_vars['features_reply']).replace(' ', '')))
        url = '{}/graphql/XjlydVWHFIDaAUny86oh2g/TweetDetail?{}'.format(self.base_url, str_vars)
        self.response = self.session.get(
            url=url,
            headers=self.__headers()
        )
        if self.response.status_code == 200:
            json_response = self.response.json()
            all_entries = json_response['data']['threaded_conversation_with_injections_v2']['instructions'][0][
                'entries']
            reply_list = [item['content']['items'][0]['item']['itemContent']['tweet_results']['result'] for item in
                          all_entries if
                          'items' in item['content'] and
                          item['content']['items'][0]['item']['itemContent']['itemType'] == 'TimelineTweet']
            next_token = next((item for item in all_entries if
                               'itemContent' in item['content'] and
                               item['content']['itemContent']['itemType'] == 'TimelineTimelineCursor' and
                               item['content']['itemContent']['cursorType'] == 'Bottom'), None)
            if next_token is not None:
                next_token = next_token['content']['itemContent']['value']
            return {"data": reply_list, 'meta': {"next_token": next_token}}
        else:
            return {"data": None, "code": self.response.status_code, "detail": self.response.text}

    def get_tweets(self, start_time=None, **kwargs):
        if 'next_token' in kwargs:
            json_vars['tweet_vars'].update({'cursor': kwargs['pagination_token']})
        if 'user_id' in kwargs:
            json_vars['tweet_vars'].update({'userId': kwargs['user_id']})

        str_vars = 'variables={}&features={}'.format(
            urllib.parse.quote(json.dumps(json_vars['tweet_vars']).replace(' ', '')),
            urllib.parse.quote(json.dumps(json_vars['features_tweet']).replace(' ', '')))
        url = '{}/graphql/juVPUUIyd5BdOivC5ROVHQ/UserTweets?{}'.format(self.base_url, str_vars)
        self.response = self.session.get(
            url=url,
            headers=self.__headers()
        )
        if self.response.status_code == 200:
            json_response = self.response.json()
            if 'data' in json_response and json_response['data']['user']['result']['timeline_v2']['timeline'][
                'instructions'][1]['type'] == 'TimelineAddEntries':
                all_entries = json_response['data']['user']['result']['timeline_v2']['timeline']['instructions'][1][
                    'entries']
                tweet_list = [item['content']['itemContent']['tweet_results']['result'] for item in all_entries if
                              'itemContent' in item['content'] and
                              item['content']['itemContent']['itemType'] == 'TimelineTweet']
                for item in tweet_list:
                    s = item['legacy']['created_at'].split(' ')
                    date = "{} {} {} {}".format(s[0], s[2], s[1], s[5])
                    time = s[3]
                    datetime_object = datetime.strptime("{} {}".format(date, time), '%a %d %b %Y %H:%M:%S')
                    if (datetime_object - start_time).seconds <= 0:
                        del item
                next_token = next((item for item in all_entries if
                                   'cursorType' in item['content'] and item['content']['cursorType'] == 'Bottom' and
                                   item['content']['entryType'] == 'TimelineTimelineCursor'), None)
                if next_token is not None:
                    next_token = next_token['content']['value']
                return {"data": tweet_list, 'meta': {"next_token": next_token}}
        else:
            return {"data": None, "code": self.response.status_code, "detail": self.response.text}
