import os

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail


class ContactTest(TestCase):
    def test_show_form(self):
        response = self.client.get(reverse("core_contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("<form", response.content)

    def test_wrong_input(self):
        response = self.client.post(reverse("core_contacts"), {
            "email": "bad email",
            "message": "",
        })
        self.assertEqual(response.status_code, 200)  # No redirect.
        self.assertEqual(len(mail.outbox), 0)

    def test_correct_input(self):
        # TODO: Add a decorator or something.
        os.environ['RECAPTCHA_TESTING'] = 'True'
        try:
            response = self.client.post(reverse("core_contacts"), {
                "email": "client@example.com",
                "message": "Build me a social site!",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(len(mail.outbox), 1)
        except Exception:
            os.environ['RECAPTCHA_TESTING'] = 'False'
            raise

    def test_captcha_works(self):
        response = self.client.post(reverse("core_contacts"), {
            "email": "client@example.com",
            "message": "Build me a social site!",
            "recaptcha_response_field": "foobar",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
