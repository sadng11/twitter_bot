from django.db import models
from django.utils.translation import gettext_lazy as _


class TwUser(models.Model):
    objects = models.Manager()
    tw_username = models.CharField(max_length=255, blank=False, default=None)
    tw_name = models.CharField(max_length=255, blank=False, default=None)
    tw_uid = models.CharField(max_length=255, blank=False, default=None)

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    def __str__(self):
        return self.tw_username
