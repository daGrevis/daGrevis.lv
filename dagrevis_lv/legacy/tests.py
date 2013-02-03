# -*- coding: utf-8 -*-
from django.test import TestCase


class RedirectTest(TestCase):
    def test_article(self):
        response = self.client.get(u"/article/42/āāēē", follow=True)
        expected = "http://testserver/blog/42/"
        actual = response.redirect_chain[-1][0]
        self.assertEqual(expected, actual)

    def test_articles_list(self):
        response = self.client.get(u"/article/list", follow=True)
        expected = "http://testserver/"
        actual = response.redirect_chain[-1][0]
        self.assertEqual(expected, actual)
