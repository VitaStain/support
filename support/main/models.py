from django.conf import settings
from django.db import models


class Ticket(models.Model):
    STATE_CHOICES = [
        ('Solved', 'sol'),
        ('Unsolved', 'unsol'),
        ('Frozen', 'fr')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    msg = models.TextField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Unsolved')


class Message(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    msg = models.TextField()
