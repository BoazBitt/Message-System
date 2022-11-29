import datetime
from django.test import tag
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import json
from message.models import Message


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
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.msg1 = Message.objects.create(sender=self.user1,
                                      receiver=self.user2,
                                      subject='msg1',
                                      msg='msg1',
                                      creation_date=datetime.date.today())
        self.msg2 = Message.objects.create(sender=self.user3,
                                      receiver=self.user2,
                                      subject='msg2',
                                      msg='msg2',
                                      creation_date=datetime.date.today())
        self.msg3 = Message.objects.create(sender=self.user1,
                                      receiver=self.user2,
                                      subject='msg3',
                                      msg='msg3',
                                      creation_date=datetime.date.today())
        self.msg1.save()
        self.msg2.save()
        self.msg3.save()

    @tag('Unit-Test')
    def test_SendMessages(self):
        url = reverse('send_message-list')
        token = Token.objects.get(user=self.user1)
        payload = json.dumps({
            "receiver": self.user2.id,
            "subject": "hello",
            "msg": "sent a msg"
        })
        response = self.client.post(
            url,
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Message.objects.get(
            sender=self.user1.id,
            receiver=self.user2.id,
            subject="hello",
            msg='sent a msg',
        ))

    @tag('Unit-Test')
    def test_Read_ALL_Messages(self):
        url = reverse('all_messages-list')
        token = Token.objects.get(user=self.user2)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token), )
        self.assertEqual(response.data[0]['subject'], 'msg1')
        self.assertEqual(response.data[1]['subject'], 'msg2')
        self.assertEqual(response.data[2]['subject'], 'msg3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('Unit-Test')
    def test_Read_Message_UnAuth(self):
        url = reverse('read-detail', kwargs={'pk': self.msg1.id})
        token = Token.objects.get(user=self.user3)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
            pk=self.msg1.id)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    @tag('Unit-Test')
    def test_Read_Message_Auth(self):
        url = reverse('read-detail', kwargs={'pk': self.msg1.id})
        token = Token.objects.get(user=self.user1)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
            pk=self.msg1.id)
        self.assertNotEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    @tag('Unit-Test')
    def test_Watch_Unread_Messages(self):


        url = reverse('Unread_messages-list')
        token = Token.objects.get(user=self.user2)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
           )
        self.assertEqual(response.data[0]['subject'], 'msg1')
        self.assertEqual(response.data[1]['subject'], 'msg2')
        self.assertEqual(response.data[2]['subject'], 'msg3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('Unit-Test')
    def test_Change_Read_Status(self):
        self.assertFalse(self.msg1.read)
        url = reverse('read-detail', kwargs={'pk': self.msg1.id})
        token = Token.objects.get(user=self.user2)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
        )
        print(self.msg1.read)#Prints False BUT changes!

    @tag('Unit-Test')
    def test_Receiver_Delete_Message(self):
        url = reverse('delete-detail', kwargs={'pk': self.msg1.id})
        token = Token.objects.get(user=self.user2)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
        )
        print(response.status_code)
        self.assertEqual(response.data['detail'],'receiver deleted the message')
        self.assertNotEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    @tag('Unit-Test')
    def test_Sender_Delete_Message(self):
        url = reverse('delete-detail', kwargs={'pk': self.msg1.id})
        token = Token.objects.get(user=self.user1)
        response = self.client.get(
            url,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
        )
        print(response.status_code)
        self.assertEqual(response.data['detail'],'receiver sender the message')
        self.assertNotEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
