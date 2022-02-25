from rest_framework import serializers

from .models import Message, Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
