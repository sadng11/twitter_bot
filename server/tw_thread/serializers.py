from rest_framework import serializers, pagination

from tw_thread.models import Tweet, Reply
from tw_user.models import TwUser


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'reply_id', 'author_id', 'tw_ref_id', 'text', 'blue_verified', 'location', 'name',
                  'screen_name',
                  'followers_count', 'friends_count', 'views', 'creat_date']


class TweetSerializer(serializers.ModelSerializer):
    def paginated_reply(self, obj):
        reply = Reply.objects.filter(tw_ref_id=obj.tw_id)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(reply, self.context['request'])
        serializer = ReplySerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data

    class Meta:
        model = Tweet
        fields = ['id', 'tw_id', 'tw_author_id', 'tw_text', 'tw_date', 'views', 'quote_count', 'reply_count',
                  'retweet_count']


class TweetDetailSerializer(serializers.ModelSerializer):
    # reply = serializers.SerializerMethodField('paginated_reply')

    def paginated_reply(self, obj):
        reply = Reply.objects.filter(tw_ref_id=obj.tw_id)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(reply, self.context['request'])
        serializer = ReplySerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data

    class Meta:
        model = Tweet
        fields = ['id', 'tw_id', 'tw_author_id', 'tw_text', 'tw_date', 'views', 'quote_count', 'reply_count',
                  'retweet_count']
