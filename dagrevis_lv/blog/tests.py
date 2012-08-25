from uuid import uuid4
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from blog.models import *
from django.template import defaultfilters


def create_user(username=None, password=None):
    username = username if username else str(uuid4())
    password = password if password else str(uuid4())
    user = User.objects.create_user(username=username, password=password)
    return user


def create_article(user=None, title=None, content=None, slug=None):
    user = user if user else create_user()
    title = title if title else str(uuid4())
    content = content if content else str(uuid4())
    slug = slug if slug else defaultfilters.slugify(str(uuid4()))
    article = Article()
    article.user = user
    article.title = title
    article.content = content
    article.slug = slug
    article.save()
    return article


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
