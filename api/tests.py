from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from api.models import Word, Proposal

CREATE_USER_URL = reverse('accounts:create')
TOKEN_URL = reverse('accounts:token')
ME_URL = reverse('accounts:me')

GENUS_URL = reverse('genera', kwargs={"lang": "d"})
FAMILY_URL = reverse('families', kwargs={"lang": "d"})
PROPOSAL_URL = reverse('proposals', kwargs={"lang":"d"})
NOTIFICATION_URL = reverse('notifications', kwargs={"lang":"d"})

WORD_URL = reverse('words', kwargs={"lang":"d"})


def create_user(**param):
    return get_user_model().objects.create_user(**param)


def create_linguist(**param):
    return get_user_model().objects.create_linguist(**param)


def create_super_user(**param):
    return get_user_model().objects.create_superuser(**param)


class PermissionTests(TestCase):
    """ Test API permissions """

    def setUp(self):

        self.normaluser = create_user(
            email = 'test@test.com',
            password = 'test123',
            name = 'name'
        )
        self.NORMALUSER = APIClient()
        self.NORMALUSER.force_authenticate(user=self.normaluser)

        self.linuser = create_linguist(
            email = 'test@linguist.com',
            password = 'test123',
            name = 'name'
        )
        self.LINGUIST = APIClient()
        self.LINGUIST.force_authenticate(user=self.linuser)

        self.superuser = create_super_user(
            email = 'test@superuser.com',
            password = 'test123',
            name = 'name'
        )
        self.SUPERUSER = APIClient()
        self.SUPERUSER.force_authenticate(user=self.superuser)

        self.UNAUTHENTICATED = APIClient()


        
    def test_user_method_forbidden(self):
        """ Test that normal user has only ReadOnly permission for families"""
        payload = {
            'name':"myFamily"
        }
        resGet = self.NORMALUSER.get(FAMILY_URL)
        self.assertEqual(resGet.status_code, status.HTTP_200_OK)

        resPost = self.NORMALUSER.post(FAMILY_URL,payload)
        self.assertEqual(resPost.status_code, status.HTTP_403_FORBIDDEN)

    def test_linguist_access_families(self):
        """ Test that linguist user has Permissions for families """
        payload = {
            'name':"myFamily"
        }

        resGet = self.LINGUIST.get(FAMILY_URL)
        self.assertEqual(resGet.status_code, status.HTTP_200_OK)

        resPost = self.LINGUIST.post(FAMILY_URL,payload)
        self.assertEqual(resPost.status_code, status.HTTP_201_CREATED)
    
    def test_proposals_have_limited_access(self):
        """ Test that proposals have limited access to authenticated users """

        resGet1 = self.LINGUIST.get(PROPOSAL_URL)
        self.assertEqual(resGet1.status_code, status.HTTP_200_OK)

        resGet2 = self.SUPERUSER.get(PROPOSAL_URL)
        self.assertEqual(resGet2.status_code, status.HTTP_200_OK)

        resGet3 = self.NORMALUSER.get(PROPOSAL_URL)
        self.assertEqual(resGet3.status_code, status.HTTP_200_OK)

        resGet4 = self.UNAUTHENTICATED.get(PROPOSAL_URL)
        self.assertEqual(resGet4.status_code, status.HTTP_403_FORBIDDEN)


    def test_notifications_have_limited_access(self):
        """ Test that notifications have limited access to authenticated users """

        resGet1 = self.LINGUIST.get(NOTIFICATION_URL)
        self.assertEqual(resGet1.status_code, status.HTTP_200_OK)

        resGet2 = self.SUPERUSER.get(NOTIFICATION_URL)
        self.assertEqual(resGet2.status_code, status.HTTP_200_OK)

        resGet3 = self.NORMALUSER.get(NOTIFICATION_URL)
        self.assertEqual(resGet3.status_code, status.HTTP_200_OK)

        resGet4 = self.UNAUTHENTICATED.get(NOTIFICATION_URL)
        self.assertEqual(resGet4.status_code, status.HTTP_403_FORBIDDEN)


    def test_proposal_add(self):
        """ Test listing new proposals """
        
        wordPayload = {
            'name':'word1',
        }
        res1 = self.LINGUIST.post(WORD_URL, wordPayload)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        wordObject = Word.objects.get(name=wordPayload['name'])
        # print(f'word: {wordObject.pk}')
        proposal_payload = {
            'word':wordObject.pk,
            'proposedWord': 'word2',
            'note': 'This is a testing proposal!'
        }

        res2 = self.NORMALUSER.post(PROPOSAL_URL, proposal_payload)

        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)

    
    def test_user_retrieve_only_owned_proposals(self):
        """ Test that users can see only the proposals that they have made """
        wordPayload = {
            'name':'word1',
        }
        res1 = self.LINGUIST.post(WORD_URL, wordPayload)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        wordObject = Word.objects.get(name=wordPayload['name'])

        proposal1_payload = {
            'word':wordObject.pk,
            'proposedWord': 'word2',
            'note': 'This is the first proposal!'
        }

        proposal2_payload = {
            'word':wordObject.pk,
            'proposedWord': 'word3',
            'note': 'This is the second proposal!'
        }

        # Create the proposals
        self.LINGUIST.post(PROPOSAL_URL, proposal1_payload)
        self.NORMALUSER.post(PROPOSAL_URL, proposal2_payload)
        # List the proposals
        res1 = self.LINGUIST.get(PROPOSAL_URL)
        res2 = self.NORMALUSER.get(PROPOSAL_URL)

        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        # Here see that different useres have different results
        self.assertNotEqual(res1.data, res2.data)