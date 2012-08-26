from uuid import uuid4
from dagrevis_lv.tests import *
from django.test import TestCase
from django.core.urlresolvers import reverse


class AuthenticationTest(TestCase):
    def test_login(self):
        # Page exists.
        response = self.client.get(reverse("user_login"))
        self.assertEqual(200, response.status_code)

        # No user.
        response = self.client.post(reverse("user_login"), {"username": str(uuid4()), "password": str(uuid4())})
        self.assertFalse(logged_in())

        # Wrong password.
        user = create_user()
        response = self.client.post(reverse("user_login"), {"username": user.username, "password": str(uuid4())})

        # All OK.
        password = str(uuid4())
        user = create_user(password=password)
        response = self.client.post(reverse("user_login"), {"username": user.username, "password": user.password})
