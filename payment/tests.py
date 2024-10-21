from django.test import TestCase
from .models import Order, Payment, Donations
from authUser.models import User, ShippingAddress, Measurement
from creators.models import Style
# Create your tests here.


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123")
        self.style = Style.objects.create(
            title="test title",
            asking_price = 100.99,
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
        self.measurement = Measurement.objects.create(
            user=self.user,
            title="Height",
            body="175cm"
        )
        self.order = Order.objects.create(
            user=self.user,
            style=self.style,
            shipp_addr=self.shipping_address,
            measurement=self.measurement,
            amount=100.99
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.style, self.style)
        self.assertEqual(self.order.shipp_addr, self.shipping_address)
        self.assertEqual(self.order.measurement, self.measurement)
        self.assertEqual(self.order.amount, 100.99)


class PaymentTestCase(TestCase):
    def setUp(self):
        """
        Payment testing
        """
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123")
        self.style = Style.objects.create(
            title="test title",
            asking_price = 100.99,
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
        self.measurement = Measurement.objects.create(
            user=self.user,
            title="Height",
            body="175cm"
        )
        self.order = Order.objects.create(
            user=self.user,
            style=self.style,
            shipp_addr=self.shipping_address,
            measurement=self.measurement,
            amount=100.99
        )
        self.payment = Payment.objects.create(
            order = self.order,
            amount = self.order.amount,
            ref = "refrence_code",
            verified = False,
        )
    
    def test_payment(self):
        """
        Payment testing
        """
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.amount, self.order.amount)
        self.assertEqual(self.payment.ref, "refrence_code")
        self.assertFalse(self.payment.verified)
    

class DonationTestCase(TestCase):
    def setUp(self):
        self.donation = Donations.objects.create(
            email="donation@email.com",
            amount= 100.00,
            ref="don_ref",
            verified=False
        )
    def test_donations(self):
        self.assertEqual(self.donation.email, "donation@email.com")
        self.assertEqual(self.donation.amount, 100.00)
        self.assertEqual(self.donation.ref, "don_ref")
        self.assertEqual(self.donation.verified, False)
