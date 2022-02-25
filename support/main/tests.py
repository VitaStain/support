from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Ticket
from rest_framework import status
from rest_framework.test import APITestCase


class SupportTest(APITestCase):
    def setUp(self):
        self.url = reverse('main:token_obtain_pair')
        self.user_test = User.objects.create_user(username='user', password='pass')
        self.user_test.save()
        self.ticket = Ticket.objects.create(msg='test', user=self.user_test)
        self.resp = self.client.post(self.url, {'username': 'user', 'password': 'pass'}, format='json')
        self.token = self.resp.data['access']
        self.data = {'msg': 'test',
                     'ticket': self.ticket.id}

    def test_get_ticket(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('main:ticket-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_ticket(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('main:ticket-list'), {'msg': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_invalid_auth(self):
        response = self.client.get(reverse('main:chat', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_invalid_auth(self):
        response = self.client.post(reverse('main:chat', kwargs={'pk': self.ticket.id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_msg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('main:chat', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_msg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('main:chat', kwargs={'pk': self.ticket.id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
