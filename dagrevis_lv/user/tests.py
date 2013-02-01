from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.models import User

from core import test_utilities


class RegistrationTest(TestCase):
    def test_fail(self):
        # No data.
        self.client.post(reverse("user_registration"))
        self.assertFalse(User.objects.all().exists())
        # Password mismatch.
        self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(length=30),
                "password1": "P4ssw0rd*",
                "password2": "P4ssw0rd",
            },
        )
        self.assertFalse(User.objects.all().exists())

    def test_success(self):
        self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(length=30),
                "password1": "P4ssw0rd*",
                "password2": "P4ssw0rd*",
            },
        )
        self.assertTrue(User.objects.all().exists())

    def test_username_remembered_when_fail(self):
        username = test_utilities.get_data(length=30)
        response = self.client.post(
            reverse("user_registration"),
            {"username": username},
        )
        self.assertIn(username, response.content)

    def test_honeypot(self):
        """Honeypot is CAPTCHA alternative."""
        response = self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(length=30),
                "password1": "P4ssw0rd*",
                "password2": "P4ssw0rd*",
                "im_bot": "on",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.all().exists())


class LoginTest(TestCase):
    def test_fail(self):
        self.client.post(reverse("user_login"), {"username": test_utilities.get_data(), "password": test_utilities.get_data()})
        logged_in = test_utilities.logged_in(self.client)
        self.assertFalse(logged_in)

    def test_success(self):
        username = test_utilities.get_data(length=16)
        password = test_utilities.get_data()
        test_utilities.create_user(username, password)
        self.client.post(reverse("user_login"), {"username": username, "password": password})
        logged_in = test_utilities.logged_in(self.client)
        self.assertTrue(logged_in)


class LogoutTest(TestCase):
    def test_success(self):
        username = test_utilities.get_data()
        password = test_utilities.get_data()
        test_utilities.create_user(username, password)
        auth.authenticate(username=username, password=password)
        self.client.get(reverse("user_logout"))
        logged_in = test_utilities.logged_in(self.client)
        self.assertFalse(logged_in)
