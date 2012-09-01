from dagrevis_lv.tests import *
from django.test import TestCase
from django.core.urlresolvers import reverse


class AuthenticationTest(TestCase):
    def test_login(self):
        # Page exists.
        response = self.client.get(reverse("user_login"))
        self.assertEqual(200, response.status_code)

        # No user.
        response = self.client.post(
            reverse("user_login"),
            {
                "username": get_data(length=30),  # Max length of username.
                "password": get_data(),
            },
        )
        self.assertFalse(logged_in(self.client))

        # Wrong password.
        username = get_data(length=30)
        create_user(username=username)
        response = self.client.post(
            reverse("user_login"),
            {
                "username": username,
                "password": get_data(),
            },
        )
        self.assertFalse(logged_in(self.client))

        # All OK.
        username = get_data(length=30)
        password = get_data()
        create_user(username=username, password=password)
        response = self.client.post(
            reverse("user_login"),
            {
                "username": username,
                "password": password,
            },
        )
        self.assertTrue(logged_in(self.client))
