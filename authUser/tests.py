from django.test import TestCase, Client
from django.urls import reverse
from .models import User, ShippingAddress, WishList, Measurement
from .forms import RegisterForm, LoginForm, ShippingAddressForm, MeasurementForm
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


##### Views Test Case ######
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

    def test_add_wishlist(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.post(reverse('add_wishlist', args=[self.style.id]))
        self.assertEqual(response.status_code, 201)
    
    def test_remove_wishlist(self):
        self.client.login(email="test@example.com", password="password123")
        self.wishlist.members.add(self.style)
        response = self.client.post(reverse('rm_wishlist', args=[self.style.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_shipping_address(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.post(reverse('shipping'), {
            'phone': '1234567890',
            'country': 'Country',
            'state': 'State',
            'lga': 'LGA',
        })
        self.assertEqual(response.status_code, 200)  # Should redirect to profile on success
    
    def test_add_measurement(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.post(reverse('measurement'), {'title': 'New Measurement', 'body': 'Details here'})
        self.assertEqual(response.status_code, 302)  # Should redirect to profile on success
    
    def test_list_orders(self):
        self.client.login(email="test@example.com", password="password123")
        response = self.client.get(reverse('list_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/orders.html')


#### Form Test ######
class FormTestCase(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'email': 'user@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertTrue(form.is_valid())
    
    def test_register_form_missing_email(self):
        form = RegisterForm(data={
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_register_form_password_mismatch(self):
        form = RegisterForm(data={
            'email': 'user@example.com',
            'password1': 'strongpassword123',
            'password2': 'differentpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class LoginFormTest(TestCase):
    def test_login_form_valid_data(self):
        form = LoginForm(data={
            'email': 'user@example.com',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())
    
    def test_login_form_missing_password(self):
        form = LoginForm(data={
            'email': 'user@example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

class ShippingAddressFormTest(TestCase):
    def test_shipping_address_form_valid_data(self):
        form = ShippingAddressForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'zip_code': '123456'
        })
        self.assertTrue(form.is_valid())
    
    def test_shipping_address_form_missing_zip_code(self):
        form = ShippingAddressForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)

class MeasurementFormTest(TestCase):
    def test_measurement_form_valid_data(self):
        form = MeasurementForm(data={
            'title': 'Waist Measurement',
            'body': '30 inches'
        })
        self.assertTrue(form.is_valid())
    
    def test_measurement_form_missing_title(self):
        form = MeasurementForm(data={
            'body': '30 inches'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


