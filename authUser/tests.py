from django.test import TestCase, Client
from django.urls import reverse
from .models import User, ShippingAddress, WishList, Measurement
from creators.models import Style
from payment.models import Order

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User")
        self.style = Style.objects.create(title="Casual")
        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist.members.add(self.style)
        self.measurement = Measurement.objects.create(
                user=self.user,
                title="Height",
                body="175cm"
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


    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.name, "Test User")
        self.assertTrue(self.user.check_password("password123"))

    def test_str_method(self):
        self.assertEqual(str(self.user), "testuser@example.com")
        
    def test_shipping_address_creation(self):
        self.assertEqual(self.shipping_address.user, self.user)
        self.assertEqual(self.shipping_address.first_name, "John")
        self.assertEqual(self.shipping_address.last_name, "Doe")
        self.assertEqual(self.shipping_address.phone, "+234123456789")

    def test_wishlist_creation(self):
        self.assertEqual(self.wishlist.user.email, self.user.email)
        self.assertIn(self.style, self.wishlist.members.all())
        self.assertEqual(str(self.wishlist), f"Wishlist of {self.user.email}")

    def test_measurement_creation(self):
        self.assertEqual(self.measurement.title, "Height")
        self.assertEqual(self.measurement.body, "175cm")
        self.assertEqual(str(self.measurement), f"Measurement of {self.user.email}")



class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                email="test@example.com", password="password123"
                )
        self.wishlist = WishList.objects.create(user=self.user)
        self.style = Style.objects.create(title="Casual")
        self.order = Order.objects.create(
                user=self.user,
                style=self.style,
                #shipp_addr=self.shipping_address,
                #measurement=self.measurement,
                amount=100.99
                )

    def test_register(self):
        response = self.client.post(reverse('register'),{'email': 'newuser@example.com', 'password': 'pass123'})
        self.assertEqual(response.status_code, 200)  # Redirect to login after registration

    def test_login_user(self):
        response = self.client.post(reverse('login_user'), {'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect on successful login

    def test_logout_user(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse('logout_user'))
        self.assertEqual(response.status_code, 302)  # Should redirect on logout

    def test_wishlist(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/wishlist.html')

    def test_profile(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

