from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('accounts:create')
TOKEN_URL = reverse('accounts:token')
ME_URL = reverse('accounts:me')

GENUS_URL = reverse('genera', kwargs={"lang": "d"})
FAMILY_URL = reverse('families', kwargs={"lang": "d"})


def create_user(**param):
    return get_user_model().objects.create_user(**param)


def create_linguist(**param):
    return get_user_model().objects.create_linguist(**param)

class PublicUserApiTests(TestCase):
    """ Test the users API """
    
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating the user with valid payload is successful """
        payload = {
            'email' : 'lazo@test.com',
            'password' : 'test123',
            'name' : 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_linguist_success(self):
        payload = {
            'email' : 'linguist@test.com',
            'password' : 'test123',
            'name' : 'Test Name',
        }

        create_linguist(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.filter(email='linguist@test.com').first()
        self.assertTrue(user.is_linguist)



    def test_user_exists(self):
        """ Test that creating an existing user fails """
        payload = {
            'email' : 'test@email.com',
            'password' : 'test123',
            'name' : 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """ Password more than 5 chars """
        payload = {
            'email' : 'test@email.com',
            'password' : 'test',
            'name' : 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """ Test that a token is created for the user """
        payload = {
            'email' : 'test@email.com',
            'password' : 'test123',
            'name' : 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentils are given """
        payload = {
            'email' : 'test@email.com',
            'password' : 'test123',
            'name' : 'Test Name'
        }
        create_user(email = 'other@email.com',password= 'test123')
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test that token is not created if user doesn't exist """
        payload = {
            'email' : 'test@email.com',
            'password' : 'test123'
        }
        res = self.client.post(TOKEN_URL, payload)  

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        payload = {
            'email' : 'test@email.com',
            'password' : ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication """

    def setUp(self):
        self.user = create_user(
            email = 'test@test.com',
            password = 'test123',
            name = 'name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_successful(self):
        """ Test retrieving profile for logged in used """
        res = self.client.get(ME_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
    
    def test_post_not_allowed(self):
        """ Test that POST is not allowed on the me url """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user"""
        payload = {
            'email' : 'test@email.com',
            'password' : 'newpass',
            'name': 'Tester New'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)