from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from core import test_utilities
from blog.models import Article


class ArticleTest(TestCase):
    def test_articles_list(self):
        # Page exists and no articles.
        response = self.client.get(reverse("blog_articles"))
        self.assertEqual(200, response.status_code)
        self.assertIn("No articles.", response.content)

        # All OK.
        article1 = test_utilities.create_article()
        article2 = test_utilities.create_article()
        response = self.client.get(reverse("blog_articles"))
        self.assertIn(article1.title, response.content)
        self.assertIn(article2.content, response.content)

    def test_single_article(self):
        # Wrong PK.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": 9999}))
        self.assertEqual(404, response.status_code)

        article = test_utilities.create_article()

        # No slug.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": article.pk}))
        self.assertEqual(301, response.status_code)

        # Wrong slug.
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": slugify(test_utilities.get_data()),
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
        article = test_utilities.create_article()
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
        article = test_utilities.create_article()

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
        test_utilities.create_and_login_user(self.client)
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": article.slug,
            },
        ))
        self.assertIn("<button>Add comment</button>", response.content)

    def test_add_comment(self):
        article = test_utilities.create_article()

        # As anonymous.
        response = self.client.post(
            reverse(
                "blog_article",
                kwargs={
                    "article_pk": article.pk,
                    "slug": article.slug,
                },
            ),
            {"content": test_utilities.get_data()},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Article.objects.get(pk=article.pk).comment_set.exists())

        # As member.
        test_utilities.create_and_login_user(self.client)
        self.client.post(
            reverse(
                "blog_article",
                kwargs={
                    "article_pk": article.pk,
                    "slug": article.slug,
                },
            ),
            {"content": test_utilities.get_data()},
        )
        self.assertEqual(Article.objects.get(pk=article.pk).comment_set.count(), 1)

    def test_nested_comments(self):
        """Testing order and depth level of comments."""
        article = test_utilities.create_article()
        comment1 = test_utilities.create_comment(article=article)
        comment2 = test_utilities.create_comment(article=article)
        comment3 = test_utilities.create_comment(article=article, parent=comment1)
        comment4 = test_utilities.create_comment(article=article, parent=comment3)
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": article.pk, "slug": article.slug}))
        expected_comments = [comment1, comment3, comment4, comment2]
        actual_comments = list(response.context[-1]["comments"])
        self.assertEqual(expected_comments, actual_comments)  # Order.
        expected_levels_of_depth = [1, 2, 3, 1]
        actual_levels_of_depth = [comment.depth for comment in actual_comments]
        self.assertEqual(expected_levels_of_depth, actual_levels_of_depth)  # Depth level.
