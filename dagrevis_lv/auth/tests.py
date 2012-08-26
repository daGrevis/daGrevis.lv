from uuid import uuid4
from dagrevis_lv.tests import *
from django.test import TestCase
from django.core.urlresolvers import reverse


class AuthenticationTest(TestCase):
    def test_login(self):
        # Page exists.
        response = self.client.get(reverse("auth_login"))
        self.assertEqual(200, response.status_code)

        # No user.
        response = self.client.post(reverse("auth_login"), {"username": str(uuid4()), "password": str(uuid4())})
        self.assertFalse(logged_in())

        # All OK.
        article1 = create_article()
        article2 = create_article()
        response = self.client.get(reverse("blog_articles"))
        self.assertIn(article1.title, response.content)
        self.assertIn(article2.content, response.content)
