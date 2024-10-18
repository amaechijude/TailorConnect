from django.test import TestCase
from .models import User, ShippingAddress, WishList, Measurement
from creators.models import Style

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.name, "Test User")
        self.assertTrue(self.user.check_password("password123"))

    def test_str_method(self):
        self.assertEqual(str(self.user), "testuser@example.com")


class ShippingAddressModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser2@example.com",
            password="password123"
        )
        self.shipping_address = ShippingAddress.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="+234123456789",
            address="123 Test St",
            country="Country",
            state="State",
            lga="LGA",
            zip_code="12345"
        )

    def test_shipping_address_creation(self):
        self.assertEqual(self.shipping_address.first_name, "John")
        self.assertEqual(self.shipping_address.last_name, "Doe")
        self.assertEqual(self.shipping_address.phone, "+234123456789")


class WishListModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="wishlistuser@example.com",
            password="password123"
        )
        self.style = Style.objects.create(title="Casual")
        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist.members.add(self.style)

    def test_wishlist_creation(self):
        self.assertEqual(self.wishlist.user.email, "wishlistuser@example.com")
        self.assertIn(self.style, self.wishlist.members.all())
        self.assertEqual(str(self.wishlist), f"Wishlist of {self.user.email}")


class MeasurementModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="measurementuser@example.com",
            password="password123"
        )
        self.measurement = Measurement.objects.create(
            user=self.user,
            title="Height",
            body="175cm"
        )

    def test_measurement_creation(self):
        self.assertEqual(self.measurement.title, "Height")
        self.assertEqual(self.measurement.body, "175cm")
        self.assertEqual(str(self.measurement), f"Measurement of {self.user.email}")
