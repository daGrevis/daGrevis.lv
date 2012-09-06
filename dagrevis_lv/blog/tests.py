from django.test import TestCase
from core.test_utilities import *
from django.core.urlresolvers import reverse
from django.template import defaultfilters
from blog.models import *


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
        response = self.client.get(reverse(
            "blog_article",
            kwargs={"article_pk": 9999},
        ))
        self.assertEqual(404, response.status_code)

        article = create_article()

        # No slug.
        response = self.client.get(reverse(
            "blog_article",
            kwargs={"article_pk": article.pk},
        ))
        self.assertEqual(301, response.status_code)

        # Wrong slug.
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": defaultfilters.slugify(get_data()),
            },
        ))
        self.assertEqual(301, response.status_code)

        # All OK.
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": article.slug,
            },
        ))
        self.assertEqual(200, response.status_code)
        self.assertIn(article.title, response.content)
        self.assertIn(article.content, response.content)


class CommentTest(TestCase):
    def test_no_comments(self):
        article = create_article()
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": article.slug,
            },
        ))
        expected = "No comments."
        self.assertIn(expected, response.content)

    def test_show_or_hide_form(self):
        article = create_article()

        # As anonymous.
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": article.slug,
            },
        ))
        expected = 'Please <a href="{}">login</a> to comment.'
        expected = expected.format(reverse("user_login"))
        self.assertIn(expected, response.content)

        # As member.
        create_and_login_user(self.client)
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": article.slug,
            },
        ))
        self.assertIn("<button>Add comment</button>", response.content)

    def test_add_comment(self):
        article = create_article()

        # As anonymous.
        response = self.client.post(
            reverse(
                "blog_article",
                kwargs={
                    "article_pk": article.pk,
                    "slug": article.slug,
                },
            ),
            {"content": get_data()},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Article.objects.get(pk=article.pk).comment_set.exists(),
        )

        # As member.
        create_and_login_user(self.client)
        self.client.post(
            reverse(
                "blog_article",
                kwargs={
                    "article_pk": article.pk,
                    "slug": article.slug,
                },
            ),
            {"content": get_data()},
        )
        self.assertEqual(
            Article.objects.get(pk=article.pk).comment_set.count(),
            1,
        )

    def test_comment_list(self):
        expected = 2
        create_and_login_user(self.client)
        article = create_article()
        for _ in range(expected):
            create_comment(article=article)
        self.assertEqual(
            Article.objects.get(pk=article.pk).comment_set.count(),
            expected,
        )
