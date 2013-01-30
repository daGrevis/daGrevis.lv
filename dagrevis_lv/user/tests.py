from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import auth

from core import test_utilities


class RegistrationTest(TestCase):
    def test_fail(self):
        # No data.
        self.client.post(reverse("user_registration"))
        self.assertFalse(auth.User.objects.all().exists())
        # Password mismatch.
        self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(),
                "password1": "P4ssw0rd*",
                "password2": "P4ssw0rd",
            },
        )
        self.assertFalse(auth.User.objects.all().exists())

    def test_success(self):
        self.client.post(
            reverse("user_registration"),
            {
                "username": test_utilities.get_data(),
                "password1": "P4ssw0rd*",
                "password2": "P4ssw0rd*",
            },
        )
        self.assertTrue(auth.User.objects.all().exists())


class LoginTest(TestCase):
    def test_fail(self):
        self.client.post(reverse("user_login"), {"username": test_utilities.get_data(), "password": test_utilities.get_data()})
        logged_in = test_utilities.logged_in(self.client)
        self.assertFalse(logged_in)

    def test_success(self):
        username = test_utilities.get_data()
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
