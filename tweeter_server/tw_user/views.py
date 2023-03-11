from rest_framework import viewsets

from tw_user.models import TwUser
from tw_user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = TwUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    http_method_names = ['get']
