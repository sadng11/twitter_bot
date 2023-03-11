from rest_framework import serializers

from tw_user.models import TwUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwUser
        fields = ['tw_username', 'tw_name', 'tw_uid']
