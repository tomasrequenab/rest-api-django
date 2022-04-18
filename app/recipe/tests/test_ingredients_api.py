from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingrendient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingrendient-list')


class PublicIngrendientsApiTests(TestCase):
    '''Test the publicly available ingrendients API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required for retrieving ingrendients'''
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngrendientsApiTests(TestCase):
    '''Test the authorized user ingrendients API'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'tomasrequenab@gmail.com',
            'Tomas123!'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingrendients(self):
        '''Test retrieving ingrendients'''
        Ingrendient.objects.create(user=self.user, name='Tomato')
        Ingrendient.objects.create(user=self.user, name='Lettuce')

        res = self.client.get(INGREDIENTS_URL)

        ingrendients = Ingrendient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingrendients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingrendients_limited_to_user(self):
        '''Test that ingrendients returned are for the authenticated user'''
        user2 = get_user_model().objects.create_user(
            'tomasrequena1994@gmail.com',
            'Tomas123!'
        )

        Ingrendient.objects.create(user=user2, name='Fruity')
        ingredient = Ingrendient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        '''Test creating a new ingredient'''
        payload = {'name': 'Test ingredient'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingrendient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        '''Test creating a new ingredient with invalid payload'''
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)