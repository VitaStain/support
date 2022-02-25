from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Message, Ticket
from .permissions import IsOwnerOrIsAdmin
from .serializers import ChatSerializer, TicketSerializer
from .tasks import send_user_email


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


class ChatViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = ChatSerializer
    permission_classes = (IsOwnerOrIsAdmin,)

    def get_queryset(self):
        queryset = Message.objects.filter(ticket=self.kwargs['pk'])
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if request.user.is_staff:
            ticket = Ticket.objects.get(id=self.kwargs['pk'])
            send_user_email.delay(ticket.user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
