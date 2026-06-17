from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal
from datetime import datetime
import pytz

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


# ─── Model tests ──────────────────────────────────────────────────────────────

class MenuModelTest(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            title='Bruschetta',
            price=Decimal('7.50'),
            inventory=50,
        )

    def test_menu_str(self):
        self.assertEqual(str(self.menu_item), 'Bruschetta : 7.50')

    def test_menu_fields(self):
        item = Menu.objects.get(title='Bruschetta')
        self.assertEqual(item.price, Decimal('7.50'))
        self.assertEqual(item.inventory, 50)


class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            name='John Doe',
            no_of_guests=4,
            booking_date=datetime(2024, 12, 25, 19, 0, tzinfo=pytz.UTC),
        )

    def test_booking_str(self):
        self.assertEqual(str(self.booking), 'John Doe')

    def test_booking_fields(self):
        b = Booking.objects.get(name='John Doe')
        self.assertEqual(b.no_of_guests, 4)


# ─── Serializer tests ─────────────────────────────────────────────────────────

class MenuSerializerTest(TestCase):
    def test_serializer_fields(self):
        item = Menu(title='Pizza', price=Decimal('12.99'), inventory=30)
        serializer = MenuSerializer(item)
        self.assertIn('title', serializer.data)
        self.assertIn('price', serializer.data)
        self.assertIn('inventory', serializer.data)

    def test_serializer_validation(self):
        data = {'title': 'Pasta', 'price': '11.50', 'inventory': 20}
        serializer = MenuSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


# ─── API tests ────────────────────────────────────────────────────────────────

class MenuAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

        self.item1 = Menu.objects.create(title='Lemon Risotto', price=Decimal('14.00'), inventory=25)
        self.item2 = Menu.objects.create(title='Greek Salad', price=Decimal('9.00'), inventory=40)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_all_menu_items_unauthenticated(self):
        """Public can list menu items."""
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_menu_item(self):
        response = self.client.get(reverse('menu-detail', args=[self.item1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Lemon Risotto')

    def test_create_menu_item_requires_auth(self):
        data = {'title': 'Tiramisu', 'price': '6.50', 'inventory': 15}
        response = self.client.post(reverse('menu-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu_item_authenticated(self):
        self._auth()
        data = {'title': 'Tiramisu', 'price': '6.50', 'inventory': 15}
        response = self.client.post(reverse('menu-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)

    def test_update_menu_item(self):
        self._auth()
        data = {'title': 'Lemon Risotto', 'price': '15.00', 'inventory': 20}
        response = self.client.put(reverse('menu-detail', args=[self.item1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.price, Decimal('15.00'))

    def test_delete_menu_item(self):
        self._auth()
        response = self.client.delete(reverse('menu-detail', args=[self.item2.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 1)

    def test_partial_update_menu_item(self):
        self._auth()
        response = self.client.patch(reverse('menu-detail', args=[self.item1.id]), {'inventory': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.inventory, 5)


class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bookinguser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.booking = Booking.objects.create(
            name='Alice',
            no_of_guests=2,
            booking_date=datetime(2024, 12, 31, 20, 0, tzinfo=pytz.UTC),
        )

    def test_list_bookings(self):
        response = self.client.get('/restaurant/booking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_booking(self):
        data = {
            'name': 'Bob',
            'no_of_guests': 6,
            'booking_date': '2025-01-15T19:00:00Z',
        }
        response = self.client.post('/restaurant/booking/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_retrieve_booking(self):
        response = self.client.get(f'/restaurant/booking/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Alice')

    def test_update_booking(self):
        data = {
            'name': 'Alice Updated',
            'no_of_guests': 3,
            'booking_date': '2024-12-31T20:00:00Z',
        }
        response = self.client.put(f'/restaurant/booking/{self.booking.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, 'Alice Updated')

    def test_delete_booking(self):
        response = self.client.delete(f'/restaurant/booking/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_requires_auth(self):
        unauthenticated = APIClient()
        response = unauthenticated.get('/restaurant/booking/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAuthAPITest(APITestCase):
    def test_register_user(self):
        data = {'username': 'newuser', 'password': 'StrongPass123!'}
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_obtain_token(self):
        User.objects.create_user(username='tokenuser', password='testpass123')
        data = {'username': 'tokenuser', 'password': 'testpass123'}
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)

    def test_current_user_endpoint(self):
        user = User.objects.create_user(username='meuser', password='testpass123')
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/restaurant/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'meuser')
