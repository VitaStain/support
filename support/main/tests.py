from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SupportTest(APITestCase):

    def test_auth(self):
        response = self.client.get(reverse('main:chat'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
