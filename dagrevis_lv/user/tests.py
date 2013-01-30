from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from core import test_utilities


class RegistrationTest(TestCase):
    def test_no_data(self):
        self.client.post(reverse("user_registration"))
        self.assertFalse(User.objects.all().exists())

    def test_password_mismatch(self):
        self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(),
                "password1": "12345",
                "password2": "1234",
            },
        )
        self.assertFalse(User.objects.all().exists())

    def test_error_message(self):
        response = self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(),
                "password1": "12345",
                "password2": "1234",
            },
            follow=True,
        )
        expected = "Passwords do not match!"
        self.assertIn(expected, response.content)

    def test_registration_success(self):
        username = test_utilities.get_data()
        self.client.post(
            reverse("user_registration"),
            {
                "username": username,
                "password1": "12345",
                "password2": "12345",
            },
        )
        self.assertTrue(User.objects.get(username=username))
