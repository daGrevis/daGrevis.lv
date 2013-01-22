from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings

from core import test_utilities
from blog.models import Article


class ArticleTest(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse("blog_articles"))
        self.assertIn("No articles.", response.content)

    def test_article_titles(self):
        article1 = test_utilities.create_article()
        article2 = test_utilities.create_article()
        response = self.client.get(reverse("blog_articles"))
        self.assertIn(article1.title, response.content)
        self.assertIn(article2.title, response.content)

    def test_sorted_articles(self):
        date1 = datetime(year=2013, month=1, day=1)
        date2 = datetime(year=2013, month=2, day=1)
        article1 = test_utilities.create_article(created=date1)
        article2 = test_utilities.create_article(created=date1)
        article3 = test_utilities.create_article(created=date2)
        response = self.client.get(reverse("blog_articles"))
        actual_articles = response.context[-1]["sorted_articles"]
        expected_articles = {}
        expected_articles[date1.year, date1.month] = [article2, article1]
        expected_articles[date2.year, date2.month] = [article3]
        self.assertEqual(expected_articles, actual_articles)

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
        response = test_utilities.request_article(self.client, article)
        self.assertEqual(200, response.status_code)
        self.assertIn(article.title, response.content)
        self.assertIn(article.content, response.content)


class CommentTest(TestCase):
    def test_no_comments(self):
        article = test_utilities.create_article()
        response = test_utilities.request_article(self.client, article)
        expected = "No comments."
        self.assertIn(expected, response.content)

    def test_show_or_hide_form(self):
        article = test_utilities.create_article()

        # As anonymous.
        response = test_utilities.request_article(self.client, article)
        expected = 'Please login with <a href="#">Twitter</a> or <a href="#">GitHub</a>, if you want to comment.'
        self.assertIn(expected, response.content)

        # As member.
        test_utilities.create_and_login_user(self.client)
        response = test_utilities.request_article(self.client, article)
        self.assertIn("<button>Add comment</button>", response.content)

    def test_add_comment(self):
        article = test_utilities.create_article()

        # As anonymous.
        response = self.client.post(article.get_link(), {"content": test_utilities.get_data()})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Article.objects.get(pk=article.pk).comment_set.exists())

        # As member.
        test_utilities.create_and_login_user(self.client)
        self.client.post(article.get_link(), {"content": test_utilities.get_data()})
        self.assertEqual(Article.objects.get(pk=article.pk).comment_set.count(), 1)

    def test_nested_comments(self):
        """Testing order and depth of comments."""
        article = test_utilities.create_article()
        comment1 = test_utilities.create_comment(article=article)
        comment2 = test_utilities.create_comment(article=article)
        comment3 = test_utilities.create_comment(article=article, parent=comment1)
        comment4 = test_utilities.create_comment(article=article, parent=comment3)
        response = test_utilities.request_article(self.client, article)
        expected_comments = [comment1, comment3, comment4, comment2]
        actual_comments = list(response.context[-1]["comments"])
        self.assertEqual(expected_comments, actual_comments)  # Order.
        expected_depth = [1, 2, 3, 1]
        actual_depth = [comment.depth for comment in actual_comments]
        self.assertEqual(expected_depth, actual_depth)  # Depth.

    def test_get_depth(self):
        comment1 = test_utilities.create_comment()
        comment2 = test_utilities.create_comment(article=comment1.article, parent=comment1)
        comment3 = test_utilities.create_comment(article=comment2.article, parent=comment2)
        self.assertEqual(1, comment1.get_depth())
        self.assertEqual(3, comment3.get_depth())

    def test_max_depth(self):
        """Tests that comment nesting isn't deeper than defined."""
        original_max = settings.MAXIMUM_DEPTH_FOR_COMMENT
        settings.MAXIMUM_DEPTH_FOR_COMMENT = 2
        article = test_utilities.create_article()
        comment1 = test_utilities.create_comment(article=article)
        comment2 = test_utilities.create_comment(article=article, parent=comment1)
        test_utilities.create_and_login_user(self.client)
        response = self.client.post(article.get_link(), {
            "content": test_utilities.get_data(),
            "comment_pk_to_reply": comment2.pk,
        })
        self.assertEqual(403, response.status_code)
        settings.MAXIMUM_DEPTH_FOR_COMMENT = original_max


class TagTest(TestCase):
    def test_no_tags(self):
        article = test_utilities.create_article()
        response = test_utilities.request_article(self.client, article)
        tags = response.context[-1]["tags"]
        self.assertEqual(0, len(tags))

    def test_has_tags(self):
        article = test_utilities.create_article()
        tag1 = test_utilities.create_tag(article)
        tag2 = test_utilities.create_tag(article)
        response = test_utilities.request_article(self.client, article)
        tags = response.context[-1]["tags"]
        self.assertEqual(tag1, tags[0])
        self.assertEqual(tag2, tags[1])

    def test_tags_displayed(self):
        article = test_utilities.create_article()
        tag = test_utilities.create_tag(article)
        response = test_utilities.request_article(self.client, article)
        self.assertIn(tag.content, response.content)


class SearchTest(TestCase):
    def _search_request(self, phrase):
        return self.client.post(reverse("blog_search"), {"phrase": phrase})

    def test_no_results(self):
        test_utilities.create_article()
        response = self._search_request(test_utilities.get_data())
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.none()
        self.assertEqual(actual_results, expected_results)

    def test_by_phrase_in_article_title(self):
        article = test_utilities.create_article(title="Spam and Eggs")
        response = self._search_request("eggs")
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.get(pk=article.pk)
        self.assertEqual(actual_results, expected_results)

    def test_by_phrase_in_article_content(self):
        article = test_utilities.create_article(content="The quick brown fox jumps over the lazy dog.")
        response = self._search_request("lazy dog")
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.get(pk=article.pk)
        self.assertEqual(actual_results, expected_results)

    def test_by_tag(self):
        article = test_utilities.create_article()
        tag = test_utilities.create_tag(article, content="spam")
        response = self._search_request(tag.content)
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.get(pk=article.pk)
        self.assertEqual(actual_results, expected_results)

    def test_by_tags(self):
        article = test_utilities.create_article()
        tag1 = test_utilities.create_tag(article, content="spam")
        tag2 = test_utilities.create_tag(article, content="eggs")
        tags = "{},{}".format(tag1.content, tag2.content)
        response = self._search_request(tags)
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.get(pk=article.pk)
        self.assertEqual(actual_results, expected_results)

    def test_by_phrase_with_regex(self):
        article = test_utilities.create_article(content="Tip #42")
        response = self._search_request("#(\d)+")
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.get(pk=article.pk)
        self.assertEqual(actual_results, expected_results)

    def test_many_results(self):
        article1 = test_utilities.create_article(title="Spam and Eggs")
        article2 = test_utilities.create_article(content="Spam, spam, spam, spam, spam...")
        response = self._search_request("spam")
        actual_results = response.context[-1]["search_results"]
        expected_results = Article.objects.filter(pk__in=[article1.pk, article2.pk])
        self.assertEqual(actual_results, expected_results)
