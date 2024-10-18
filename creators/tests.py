from django.test import TestCase
from .models import Designer, Style, StyleImage
from authUser.models import User

# Create your tests here.

class DesignerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password@123",
            name="Test name"
        )
        self.designer = Designer.objects.create(
            user=self.user,
            brand_name="Test Brand",
            brand_email="brand@email.com",
            brand_bio="Brand Bio",
            # brand_logo="",
            brand_location="Location",
            brand_phone="0123456789", 
        )

    def test_create_designer(self):
        self.assertEqual(self.designer.user, self.user)
        self.assertEqual(self.designer.brand_name, "Test Brand")
        self.assertEqual(self.designer.brand_email, "brand@email.com")
        self.assertEqual(self.designer.brand_bio, "Brand Bio")
        self.assertEqual(self.designer.brand_location, "Location")
        self.assertEqual(self.designer.brand_phone, "0123456789")


class StyleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password@123",
            name="Test name"
        )
        self.designer = Designer.objects.create(
            user=self.user,
            brand_name="Test Brand",
            brand_email="brand@email.com",
            brand_bio="Brand Bio",
            # brand_logo="",
            brand_location="Location",
            brand_phone="0123456789", 
        )
        self.style = Style.objects.create(
            designer = self.designer,
            title = "test title",
            description = "test description",
            asking_price = 4999.99
        )

    def test_style_model(self):
        self.assertEqual(self.style.designer, self.designer)
        self.assertEqual(self.style.title, "test title")
        self.assertEqual(self.style.description, "test description")
        self.assertEqual(self.style.asking_price, 4999.99)


class StyleImageTestCAse(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="password@123",
            name="Test name"
        )
        self.designer = Designer.objects.create(
            user=self.user,
            brand_name="Test Brand",
            brand_email="brand@email.com",
            brand_bio="Brand Bio",
            # brand_logo="",
            brand_location="Location",
            brand_phone="0123456789", 
        )
        self.style = Style.objects.create(
            designer = self.designer,
            title = "test title",
            description = "test description",
            asking_price = 4999.99
        )
        self.style_image = StyleImage.objects.create(
            style=self.style,
            image=""
        )
    
    def test_style_image(self):
        self.assertEqual(self.style_image.style, self.style)