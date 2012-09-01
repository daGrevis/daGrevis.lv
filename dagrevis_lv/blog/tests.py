from uuid import uuid4
from dagrevis_lv.tests import *
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import defaultfilters


class ArticleTest(TestCase):
    def test_articles_list(self):
        # Page exists and no articles.
        response = self.client.get(reverse("blog_articles"))
        self.assertEqual(200, response.status_code)
        self.assertIn("No articles.", response.content)

        # All OK.
        article1 = create_article()
        article2 = create_article()
        response = self.client.get(reverse("blog_articles"))
        self.assertIn(article1.title, response.content)
        self.assertIn(article2.content, response.content)

    def test_single_article(self):
        # Wrong PK.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": 9999}))
        self.assertEqual(404, response.status_code)

        article = create_article()

        # No slug.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": article.pk}))
        self.assertEqual(301, response.status_code)

        # Wrong slug.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": article.pk, "slug": defaultfilters.slugify(str(uuid4()))}))
        self.assertEqual(301, response.status_code)

        # All OK.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": article.pk, "slug": article.slug}))
        self.assertEqual(200, response.status_code)
        self.assertIn(article.title, response.content)
        self.assertIn(article.content, response.content)


class CommentTest(TestCase):
    pass
