from django.test import TestCase, tag
from django.urls import reverse


class RegistrationTests(TestCase):
    @tag('Unit-Test')
    def test_register(self):
        data = {"email": "testcase@gmail.com",
                "username": "test",
                "password": "123456Tc",
                "password2": "123456Tc"}
        url = reverse('register')
        response = self.client.post(url, data)
        self.assertEqual(response.data['response'], 'User is registered successfully')
        self.assertEqual(response.status_code, 200)

    @tag('Unit-Test')
    def test_register_inValid_Email(self):
        data = {"email": "testcasegmail.com",
                "username": "test",
                "password": "123456Tc",
                "password2": "123456Tc"}
        url = reverse('register')
        response = self.client.post(url, data)
        self.assertEqual(str(response.data['email'][0]), 'Enter a valid email address.')

    @tag('Unit-Test')
    def test_register_inValid_Password(self):
        data = {"email": "testcase@gmail.com",
                "username": "test",
                "password": "123456",
                "password2": "123456Tc"}
        url = reverse('register')
        response = self.client.post(url, data)
        self.assertEqual(str(response.data['password']), 'password do not match')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 400)
