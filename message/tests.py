import json

from django.test import TestCase, tag, Client
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .models import Message
from .serializer import SendMessageSerializer
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class MessagesTestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        data1 = {"email": "test1case@gmail.com",
                 "username": "test1",
                 "password": "123456Tc",
                 "password2": "123456Tc"}
        data2 = {"email": "test2case@gmail.com",
                 "username": "test2",
                 "password": "123456Tc",
                 "password2": "123456Tc"}
        data3 = {"email": "test3case@gmail.com",
                 "username": "test3",
                 "password": "123456Tc",
                 "password2": "123456Tc"}
        self.user1 = User.objects.create_user(data1)
        self.user2 = User.objects.create_user(data2)
        self.user3 = User.objects.create_user(data3)
        self.user.save()
        self.user2.save()
        self.user3.save()
        # assure login
        logged_in = self.client.login(username='test1', password='123456Tc')
        print('**********************************************',logged_in)
        self.assertTrue(logged_in)

    # def test_SendMessages(self):
    #     def test_request_without_client():
    #         msg = {
    #             "receiver": self.user2.id,
    #             "subject": "my first message",
    #             "msg": "hello this is my first"}
    #         unknownClient = APIClient()
    #         response = unknownClient.post(reverse('send_message-list'),data=msg)
    #
    #         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #

#
# class TestViews(APITestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         url = reverse('register')
#         data1 = {"email": "test1case@gmail.com",
#                 "username": "test1",
#                 "password": "123456Tc",
#                 "password2": "123456Tc"}
#         data2 = {"email": "test2case@gmail.com",
#                 "username": "test2",
#                 "password": "123456Tc",
#                 "password2": "123456Tc"}
#         data3 = {"email": "test3case@gmail.com",
#                 "username": "test3",
#                 "password": "123456Tc",
#                 "password2": "123456Tc"}
#         cls.user1 = User.objects.create_user(data1)
#         cls.user2 = User.objects.create_user(data2)
#         cls.user3 = User.objects.create_user(data3)
#         logged_in = cls.client.login(username='testerFinal', password='testpassword')
#
#
#     def test_number_one(self):
#         self.client = APIClient()
#
#         token1 = Token.objects.get(user= self.user1)
#
#         msg = {
#                 "receiver": self.user2.id,
#                 "subject": "my first message",
#                 "msg": "hello this is my first"}
#         response = self.client.post('/api/v1/oauth2/token/', msg)
#         self.access_token = str(token1)
#         response =self.client.post(reverse('send_message-list'), headers={'Authorization': 'Token'.format(self.access_token)})
#         print(response.data)
#
#
#
#         serialzer = SendMessageSerializer(msg)
#         headers = {'Authorization':'Token' + str(token1)}
#         self.client.credentials(**headers)
# response = self.client.post(
#     reverse('send_message-list'),
#     data=serialzer,
#     content_type='application/json',
#     **{'HTTP_AUTHORIZATION': f'Bearer {token1}'}
# )m
# r = self.client.post(reverse('send_message-list'), data=msg, format='json',
#                  follow=True)
# print(r.data)
# print (self.client)
# self.client.credentials(
#     HTTP_AUTHORIZATION='Bearer ' + token1)
# response = self.client.post(url,msg)
# print(response.data)


# class SendMessageTests(TestCase):
#     def setUp(self):
#
#
#     def test_Send_Message(self):
#
#
#         print(response)
