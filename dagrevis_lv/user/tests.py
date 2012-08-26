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
        response = self.client.post(reverse("user_login"), {"username": str(uuid4())[:30], "password": str(uuid4())})
        self.assertFalse(logged_in(self.client))

        # Wrong password.
        username = str(uuid4())[:30]
        create_user(username=username)
        response = self.client.post(reverse("user_login"), {"username": username, "password": str(uuid4())})
        self.assertFalse(logged_in(self.client))

        # All OK.
        username = str(uuid4())[:30]
        password = str(uuid4())
        create_user(username=username, password=password)
        response = self.client.post(reverse("user_login"), {"username": username, "password": password})
        self.assertTrue(logged_in(self.client))
