from django.test import TestCase
from .models import Designer, Style, StyleImage, Review
from authUser.models import User

# Create your tests here.
class DesignerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="designer@example.com", password="password123")

    def test_create_designer(self):
        designer = Designer.objects.create(
            user=self.user,
            brand_name="Fashion Brand",
            brand_email="brand@example.com",
            brand_phone="1234567890"
        )
        self.assertEqual(designer.brand_name, "Fashion Brand")
        self.assertEqual(designer.is_verified, Designer.Status.NO)
        self.assertEqual(str(designer), "Fashion Brand")

class StyleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="designer@example.com", password="password123")
        self.designer = Designer.objects.create(
            user=self.user,
            brand_name="Fashion Brand",
            brand_email="brand@example.com",
            brand_phone="1234567890"
        )

    def test_create_style(self):
        style = Style.objects.create(
            designer=self.designer,
            title="Elegant Dress",
            description="A beautiful evening dress",
            likes=10,
            asking_price=200.00
        )
        self.assertEqual(style.title, "Elegant Dress")
        self.assertEqual(style.status, Style.Status.DRAFT)
        self.assertEqual(style.can_request, Style.rStatus.No)
        self.assertEqual(str(style), "Elegant Dress --- created_by  Fashion Brand")

class StyleImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="designer@example.com", password="password123")
        self.designer = Designer.objects.create(
            user=self.user,
            brand_name="Fashion Brand",
            brand_email="brand@example.com",
            brand_phone="1234567890"
        )
        self.style = Style.objects.create(
            designer=self.designer,
            title="Elegant Dress",
            description="A beautiful evening dress"
        )

    def test_create_style_image(self):
        image = StyleImage.objects.create(
            style=self.style,
            image="path/to/image.jpg"
        )
        self.assertEqual(image.style, self.style)
        self.assertEqual(str(image), "Images for Elegant Dress")

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="reviewer@example.com", password="password123")
        self.designer = Designer.objects.create(
            user=self.user,
            brand_name="Fashion Brand",
            brand_email="brand@example.com",
            brand_phone="1234567890"
        )
        self.style = Style.objects.create(
            designer=self.designer,
            title="Elegant Dress",
            description="A beautiful evening dress"
        )

    def test_create_review(self):
        review = Review.objects.create(
            user=self.user,
            style=self.style,
            text_content="Amazing dress!",
            image="path/to/review_image.jpg"
        )
        self.assertEqual(review.style, self.style)
        self.assertEqual(review.user, self.user)
        self.assertEqual(str(review), "Review on Elegant Dress")
