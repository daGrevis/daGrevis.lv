from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail


class FreelanceTest(TestCase):
    def test_show_form(self):
        response = self.client.get(reverse("core_freelance"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("<form", response.content)

    def test_wrong_input(self):
        response = self.client.post(reverse("core_freelance"), {
            "client_email": "bad email",
            "message": "",
        })
        self.assertEqual(response.status_code, 200)  # No redirect.
        self.assertEqual(len(mail.outbox), 0)

    def test_correct_input(self):
        response = self.client.post(reverse("core_freelance"), {
            "client_email": "client@example.com",
            "message": "Build me a social site!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
