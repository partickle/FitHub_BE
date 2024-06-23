from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from authorisation.models import ActivationCode

User = get_user_model()


class RegisterAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword123',
            'profile': {
                'is_male': True,
                'age': 25,
                'goal': 'gain_weight',
                'physical_activity_level': 'beginner'
            }
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'not-an-email'
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123'
        )
        self.valid_credentials = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        self.invalid_credentials = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }

    def test_login_user_success(self):
        response = self.client.post(self.url, self.valid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], self.valid_credentials['email'])

    def test_login_user_invalid_credentials(self):
        response = self.client.post(self.url, self.invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid Credentials')


class SendActivationCodeViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('send-activation-code')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123'
        )

    def test_send_activation_code_success(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Activation code sent to email')

    def test_send_activation_code_user_not_found(self):
        response = self.client.post(self.url, {'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'User with this email does not exist')


class VerifyActivationCodeViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('verify-activation-code')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123'
        )
        self.activation_code = ActivationCode.objects.create(user=self.user, code='123456')

    def test_verify_activation_code_success(self):
        response = self.client.post(self.url, {'user_id': self.user.id, 'code': '123456'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Activation code is valid.')

    def test_verify_activation_code_invalid(self):
        response = self.client.post(self.url, {'user_id': self.user.id, 'code': 'wrongcode'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid or expired activation code.')
