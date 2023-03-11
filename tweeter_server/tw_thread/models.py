from django.db import models
from django.utils.translation import gettext_lazy as _


class Tweet(models.Model):
    objects = models.Manager()
    tw_id = models.CharField(max_length=255, blank=False, default=None, unique=True)
    tw_author_id = models.CharField(max_length=255, blank=False, default=None)
    tw_text = models.TextField(blank=False, default=None)
    tw_date = models.DateTimeField(blank=False, default=None)
    views = models.IntegerField(blank=False, default=None)
    quote_count = models.IntegerField(blank=False, default=None)
    reply_count = models.IntegerField(blank=False, default=None)
    retweet_count = models.IntegerField(blank=False, default=None)

    class Meta:
        db_table = 'tweets'
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')
        ordering = ['-id']


class Reply(models.Model):
    objects = models.Manager()
    reply_id = models.CharField(max_length=255, blank=False, default=None)
    author_id = models.CharField(max_length=255, blank=False, default=None)
    tw_ref = models.ForeignKey(Tweet, on_delete=models.DO_NOTHING, blank=False, default=None,
                               to_field='tw_id')
    text = models.TextField(blank=False, default=None)
    blue_verified = models.BooleanField(blank=False, default=None)
    location = models.CharField(max_length=300, blank=False, default=None)
    name = models.CharField(max_length=300, blank=False, default=None)
    screen_name = models.CharField(max_length=300, blank=False, default=None)
    followers_count = models.IntegerField(blank=False, default=None)
    friends_count = models.IntegerField(blank=False, default=None)
    views = models.IntegerField(blank=False, default=None)
    creat_date = models.DateTimeField(blank=False, default=None)

    class Meta:
        db_table = 'reply'
        verbose_name = _('Reply')
        verbose_name_plural = _('Reply')
        ordering = ['-id']

    def __str__(self):
        return self.reply_id
