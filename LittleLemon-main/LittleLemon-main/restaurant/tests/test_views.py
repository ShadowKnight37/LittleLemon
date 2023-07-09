from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class MenuItemsViewTest(APITestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(title='Pizza', price=9.99, inventory=40)
        self.url = reverse('menuitems-list')  # Replace 'menuitems-list' with the actual URL name or pattern
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
    
    def test_list_menu_items(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_menu_item(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        data = {'title': 'Burger', 'price': 7.99, 'inventory': 60}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)

    def test_retrieve_menu_item(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        detail_url = reverse('menuitems-detail', kwargs={'pk': self.menu_item.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pizza')