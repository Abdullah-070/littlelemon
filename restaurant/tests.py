from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Menu, Booking
from datetime import date


class MenuTest(TestCase):
    def setUp(self):
        # Create test menu items
        Menu.objects.create(title="IceCream", price=80, inventory=100)
        Menu.objects.create(title="Pizza", price=120, inventory=50)
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_getall(self):
        """Test retrieving all menu items"""
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_menu_item(self):
        """Test creating a menu item"""
        data = {
            'title': 'Burger',
            'price': 95.00,
            'inventory': 30
        }
        response = self.client.post('/api/menu/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)

    def test_get_single_menu_item(self):
        """Test retrieving a single menu item"""
        menu_item = Menu.objects.get(title="IceCream")
        response = self.client.get(f'/api/menu/{menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'IceCream')

    def test_update_menu_item(self):
        """Test updating a menu item"""
        menu_item = Menu.objects.get(title="IceCream")
        data = {
            'title': 'IceCream',
            'price': 90.00,
            'inventory': 100
        }
        response = self.client.put(f'/api/menu/{menu_item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        menu_item.refresh_from_db()
        self.assertEqual(menu_item.price, 90.00)

    def test_delete_menu_item(self):
        """Test deleting a menu item"""
        menu_item = Menu.objects.get(title="IceCream")
        response = self.client.delete(f'/api/menu/{menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 1)


class BookingTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test booking
        Booking.objects.create(
            first_name='John',
            reservation_date=date(2025, 12, 25),
            reservation_slot=18
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_getall_bookings(self):
        """Test retrieving all bookings"""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        """Test creating a booking"""
        data = {
            'first_name': 'Jane',
            'reservation_date': '2025-12-26',
            'reservation_slot': 19
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_duplicate_booking_prevention(self):
        """Test that duplicate bookings are prevented"""
        data = {
            'first_name': 'Jane',
            'reservation_date': '2025-12-25',
            'reservation_slot': 18
        }
        response = self.client.post('/api/bookings/', data)
        # Should fail due to unique_together constraint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access API"""
        client = APIClient()  # New client without authentication
        response = client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_authentication(self):
        """Test user can get authentication token"""
        # Create user
        User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
        
        # Get token
        data = {
            'username': 'authuser',
            'password': 'authpass123'
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)