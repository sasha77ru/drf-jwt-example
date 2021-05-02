from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.utils import json


class MyTestCase(TestCase):
    def test_my(self):
        c = Client()

        # Create a user
        user = User.objects.create_user('joe', 'joe@doe.com', 'doe', first_name="John", is_staff=True)

        # Get tokens
        response = c.post('/api/token/', {'username': 'joe', 'password': 'doe'})
        self.assertEqual(response.status_code, 200)
        foo = json.loads(response.content.decode('utf-8'))
        refresh = foo["refresh"]
        access = foo["access"]

        # Works fine
        response = c.get('/hello/', HTTP_AUTHORIZATION="Bearer "+access)
        print(response.content)
        self.assertEqual(response.status_code, 200)

        # Refresh tokens
        response = c.post('/api/token/refresh/', data={"refresh": refresh})
        self.assertEqual(response.status_code, 200)
        foo = json.loads(response.content.decode('utf-8'))
        refresh = foo["refresh"]
        access = foo["access"]

        # Works fine
        response = c.get('/hello/', HTTP_AUTHORIZATION="Bearer "+access)
        print(response.content)
        self.assertEqual(response.status_code, 200)

        # Doesn't work with wrong token
        response = c.get('/hello/', **{"HTTP_AUTHORIZATION": "Bearer "+refresh})
        self.assertEqual(response.status_code, 401)

        # Drop user
        user.delete()

        # BUT STILL works fine
        response = c.get('/hello/', HTTP_AUTHORIZATION="Bearer "+access)
        print(response.content)
        self.assertEqual(response.status_code, 200)

        # Impossible to get tokens for deleted user
        response = c.post('/api/token/', {'username': 'joe', 'password': 'doe'})
        self.assertEqual(response.status_code, 401)

        # Impossible to refresh tokens for deleted user
        response = c.post('/api/token/refresh/', data={"refresh": refresh})
        self.assertEqual(response.status_code, 401)

        # Create an inactive user
        user = User.objects.create_user('joe', 'joe@doe.com', 'doe', is_active=False)

        # Impossible to get tokens for inactive user
        response = c.post('/api/token/', {'username': 'joe', 'password': 'doe'})
        self.assertEqual(response.status_code, 401)

        # Impossible to refresh tokens for inactive user
        response = c.post('/api/token/refresh/', data={"refresh": refresh})
        self.assertEqual(response.status_code, 401)

        # Make the user active
        user.is_active = True
        user.save()

        # Get tokens
        response = c.post('/api/token/', {'username': 'joe', 'password': 'doe'})
        self.assertEqual(response.status_code, 200)
        foo = json.loads(response.content.decode('utf-8'))
        refresh = foo["refresh"]
        access = foo["access"]

        # Works fine
        response = c.get('/hello/', HTTP_AUTHORIZATION="Bearer "+access)
        print(response.content)
        self.assertEqual(response.status_code, 200)

        # Change first_name
        user.first_name = "Johny"
        user.save()

        # Refresh tokens
        response = c.post('/api/token/refresh/', data={"refresh": refresh})
        self.assertEqual(response.status_code, 200)
        foo = json.loads(response.content.decode('utf-8'))
        refresh = foo["refresh"]
        access = foo["access"]

        # Works fine. New first_name is got from token after refresh
        response = c.get('/hello/', HTTP_AUTHORIZATION="Bearer "+access)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        foo = json.loads(response.content.decode('utf-8'))
        self.assertEqual(foo["user"]["first_name"],"Johny")