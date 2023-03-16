import os
import subprocess

import requests
import tweepy
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from decouple import config

from tw_thread.models import Process
from tw_user.models import TwUser
from tw_user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = TwUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    http_method_names = ['get']

    @action(methods=["GET"], detail=True, )
    def run(self, request, pk=None):
        if config('PROXY', default=False, cast=bool):
            os.environ['http_proxy'] = 'http://127.0.0.1:8889'
            os.environ['https_proxy'] = 'http://127.0.0.1:8889'

        client = tweepy.Client(
            bearer_token=config('BEARER_TOKEN'),
            consumer_key=config('CONSUMER_KEY'),
            consumer_secret=config('CONSUMER_SECRET'),
            access_token=config('ACCESS_TOKEN'),
            access_token_secret=config('ACCESS_TOKEN_SECRET'),
            return_type=requests.Response,
            wait_on_rate_limit=True)

        try:
            user_data_res = client.get_user(username=pk)
            user_data = user_data_res.json()['data']
            tw_user = TwUser.objects.filter(tw_uid=user_data['id']).first()
            if tw_user is None:
                TwUser.objects.create(tw_username=user_data['username'], tw_name=user_data['name'],
                                      tw_uid=user_data['id'])
            process = Process.objects.filter(tw_user_id=user_data['id']).first()
            subprocess.Popen(['kill', process.pid])
            Process.objects.filter(tw_user_id=user_data['id']).delete()
            subprocess.Popen(
                ["python", '../fetch_tweet.py', '--user_id', user_data['id']])
            return Response({"run": "OK"})
        except Exception as e:
            return Response({"error": e})
