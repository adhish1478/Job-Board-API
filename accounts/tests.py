from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from django.urls import reverse

# Create your tests here.

class AccountsAPITestCase(APITestCase):

    def setUp(self):
        self.email= 'testuser@example.com'
        self.password= 'TestPass123'

        # Create user once here for token tests
        if not CustomUser.objects.filter(email= self.email).exists():
            CustomUser.objects.create_user(
                email=self.email,
                password= self.password
            )
            
    def test_register_user(self):
        url= reverse('register')
        data={
            'email': 'newuser@example.com',
            'password': 'NewPass123'
        }
        response= self.client.post(url, data, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email= data['email']).exists())

        # Delete the user after test
        CustomUser.objects.filter(email= data['email']).delete()

    def test_token_obtain(self):
        url= reverse('token_obtain_pair')
        data={
            'email':self.email,
            'password': self.password
        }

        response= self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)