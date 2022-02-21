import json

import redis
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        SAVE = ['list', 'retrieve', 'create']
        if self.action in SAVE:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chat(request, *args, **kwargs):
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0)
    user = request._user

    if request.method == 'GET':
        items = {}
        if user.is_staff:
            for key in redis_instance.keys("*"):
                items[key.decode("utf-8")] = redis_instance.get(key)
        else:
            for key in redis_instance.keys("*"):
                if key.decode("utf-8") == user.username or key.decode("utf-8") == 'support: ' + user.username:
                    items[key.decode("utf-8")] = redis_instance.get(key)
        response = {
            'items': items
        }
        return Response(response, 200)

    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        if user.is_staff:
            name = 'support: ' + key
            value = item[key]
        else:
            name = user.username
            value = key + ': ' + item[key]
        redis_instance.set(name, value)
        response = {
            f"{name}: {value}"
        }
        return Response(response, 201)
