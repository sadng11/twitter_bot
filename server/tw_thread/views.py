from rest_framework import viewsets
from rest_framework.response import Response
from itertools import groupby
from operator import itemgetter
from tw_thread.models import Tweet, Reply
from tw_thread.serializers import TweetSerializer, TweetDetailSerializer, ReplySerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-id')
    serializer_class = TweetSerializer
    http_method_names = ['get']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Tweet.objects.order_by('-id').all()
        tw_author_id = self.request.query_params.get('tw_author_id', None)
        if tw_author_id is not None:
            queryset = queryset.filter(tw_author_id=tw_author_id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TweetDetailSerializer(instance)
        return Response(serializer.data)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all().order_by('-id')
    serializer_class = ReplySerializer
    http_method_names = ['get']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Reply.objects.all()
        tweet_id = self.request.query_params.get('tweet_id', None)
        if tweet_id is not None:
            queryset = queryset.filter(tw_ref=tweet_id)
        return queryset


class AudienceViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.filter(tw_author_id='813286').all()

    def get_serializer_class(self):
        return TweetDetailSerializer

    def list(self, request, *args, **kwargs):
        twitter = Tweet.objects.filter(tw_author_id='813286').all()
        check_list = []
        first_list = []
        for index, item in enumerate(twitter):
            tweet_ids = list(
                Reply.objects.filter(tw_ref_id=item.tw_id).values(
                    *['author_id', 'blue_verified', 'name', 'screen_name']))
            if index == 0:
                first_list = tweet_ids
            else:
                check_list.append(tweet_ids)
        final_res = []
        first_list_list = list(dict.fromkeys([sad['author_id'] for sad in first_list]))
        for index, itme_first in enumerate(first_list_list):
            res_user = {"user_id": first_list[index], "user_au": 1}
            for each in check_list:
                check_list_current = [sad['author_id'] for sad in each]
                if itme_first in check_list_current:
                    inc_user_au = res_user['user_au'] + 1
                    res_user.update({"user_au": inc_user_au})
            final_res.append(res_user)
        final_res.sort(key=itemgetter('user_au'), reverse=True)

        s = groupby(final_res, key=itemgetter('user_au'))

        fin_res = []
        for key, value in s:
            items = []
            percent_aud = round(key * 100 / len(twitter), 2)
            if percent_aud >= 50:
                for k in value:
                    items.append(k['user_id'])
                fin_res.append({"users": items, 'percent': percent_aud})
        return Response(fin_res)
