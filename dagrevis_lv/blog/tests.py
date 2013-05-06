from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test.utils import override_settings
from django.conf import settings

from core import test_utils
from blog.models import Article, Comment


class ArticleTest(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse("blog_articles"))
        self.assertIn("No articles.", response.content)

    def test_article_titles(self):
        article1 = test_utils.create_article()
        article2 = test_utils.create_article()
        response = self.client.get(reverse("blog_articles"))
        self.assertIn(article1.title, response.content)
        self.assertIn(article2.title, response.content)

    def test_sorted_articles(self):
        date1 = datetime(year=2013, month=1, day=1)
        date2 = datetime(year=2013, month=2, day=1)
        article1 = test_utils.create_article(created=date1)
        article2 = test_utils.create_article(created=date1)
        article3 = test_utils.create_article(created=date2)
        response = self.client.get(reverse("blog_articles"))
        expected_articles = {}
        expected_articles[date1.year, date1.month] = [article2, article1]
        expected_articles[date2.year, date2.month] = [article3]
        actual_articles = response.context[-1]["sorted_articles"]
        self.assertEqual(expected_articles, actual_articles)

    def test_single_article(self):
        # Wrong PK.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": 9999}))
        self.assertEqual(404, response.status_code)

        article = test_utils.create_article()

        # No slug.
        response = self.client.get(reverse("blog_article", kwargs={"article_pk": article.pk}))
        self.assertEqual(301, response.status_code)

        # Wrong slug.
        response = self.client.get(reverse(
            "blog_article",
            kwargs={
                "article_pk": article.pk,
                "slug": slugify(test_utils.get_data()),
            },
        ))
        self.assertEqual(301, response.status_code)

        # All OK.
        response = test_utils.request_article(self.client, article)
        self.assertEqual(200, response.status_code)
        self.assertIn(article.title, response.content)
        self.assertIn(article.content, response.content)

    def test_articles_feed(self):
        article = test_utils.create_article()
        response = self.client.get(reverse("blog_articles_rss_feed"))
        self.assertIn(article.title, response.content)

    def test_xss_vulnerability(self):
        content = "<script>alert('foo')</script>"
        article = test_utils.create_article(content=content)
        expected = "<p>&lt;script&gt;alert(&lsquo;foo&rsquo;)&lt;/script&gt;</p>"
        actual = article.get_content_as_html()
        self.assertEqual(expected, actual)

    def test_tweet_link(self):
        article = test_utils.create_article(tweet_id=42)
        response = test_utils.request_article(self.client, article)
        expected = article.get_tweet_link()
        actual = response.content
        self.assertIn(expected, actual)

    def test_draft_open(self):
        article = test_utils.create_article()
        response = test_utils.request_article(self.client, article)
        self.assertEqual(response.status_code, 200)
        article = test_utils.create_article(is_draft=True)
        response = test_utils.request_article(self.client, article)
        self.assertEqual(response.status_code, 404)


class CommentTest(TestCase):
    def test_no_comments(self):
        article = test_utils.create_article()
        response = test_utils.request_article(self.client, article)
        expected = "No comments."
        self.assertIn(expected, response.content)

    def test_show_or_hide_form(self):
        article = test_utils.create_article()
        # As anonymous.
        response = test_utils.request_article(self.client, article)
        expected = "Please login"
        self.assertIn(expected, response.content)
        # As member.
        test_utils.create_and_login_user(self.client)
        response = test_utils.request_article(self.client, article)
        self.assertIn("<button>Add comment</button>", response.content)

    def test_add_comment(self):
        article = test_utils.create_article()
        # As anonymous.
        response = self.client.post(
            article.get_absolute_url(),
            {
                "article": article.pk,
                "content": test_utils.get_data(),
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Article.objects.get(pk=article.pk).comment_set.exists())
        # As member.
        test_utils.create_and_login_user(self.client)
        response = self.client.post(
            article.get_absolute_url(),
            {
                "article": article.pk,
                "content": test_utils.get_data(),
            }
        )
        self.assertTrue(Article.objects.get(pk=article.pk).comment_set.exists())

    def test_nested_comments(self):
        """Testing order and depth of comments."""
        article = test_utils.create_article()
        comment1 = test_utils.create_comment(article=article)
        comment2 = test_utils.create_comment(article=article)
        comment3 = test_utils.create_comment(article=article, parent=comment1)
        comment4 = test_utils.create_comment(article=article, parent=comment3)
        response = test_utils.request_article(self.client, article)
        expected_comments = [comment1, comment3, comment4, comment2]
        actual_comments = list(response.context[-1]["article"].get_comments())
        self.assertEqual(expected_comments, actual_comments)  # Order.
        expected_depth = [1, 2, 3, 1]
        actual_depth = [comment.depth for comment in actual_comments]
        self.assertEqual(expected_depth, actual_depth)  # Depth.

    def test_get_depth(self):
        comment1 = test_utils.create_comment()
        comment2 = test_utils.create_comment(article=comment1.article, parent=comment1)
        comment3 = test_utils.create_comment(article=comment2.article, parent=comment2)
        self.assertEqual(1, comment1.get_depth())
        self.assertEqual(3, comment3.get_depth())

    @override_settings(MAX_DEPTH_FOR_COMMENT=2)
    def test_max_depth(self):
        """Tests that comment nesting isn't deeper than defined."""
        article = test_utils.create_article()
        comment1 = test_utils.create_comment(article=article)
        comment2 = test_utils.create_comment(article=article, parent=comment1)
        test_utils.create_and_login_user(self.client)
        self.client.post(article.get_absolute_url(), {
            "content": test_utils.get_data(),
            "comment_pk": comment2.pk,
        })
        self.assertEqual(Comment.objects.count(), settings.MAX_DEPTH_FOR_COMMENT)

    def test_comments_feed(self):
        comment = test_utils.create_comment()
        response = self.client.get(reverse("blog_comments_rss_feed"))
        self.assertIn(comment.content, response.content)

    def test_xss_vulnerability(self):
        content = "<script>alert('foo')</script>"
        comment = test_utils.create_comment(content=content)
        expected = "<p>&lt;script&gt;alert(&lsquo;foo&rsquo;)&lt;/script&gt;</p>"
        actual = comment.get_content_as_html()
        self.assertEqual(expected, actual)

    def test_comment_draft(self):
        article = test_utils.create_article(is_draft=True)
        test_utils.create_and_login_user(self.client)
        response = self.client.post(article.get_absolute_url(), {
            "content": test_utils.get_data(),
        })
        self.assertEqual(response.status_code, 404)


class TagTest(TestCase):
    def test_no_tags(self):
        article = test_utils.create_article()
        response = test_utils.request_article(self.client, article)
        tags = response.context[-1]["article"].tag_set.all()
        self.assertEqual(0, len(tags))

    def test_has_tags(self):
        article = test_utils.create_article()
        tag1 = test_utils.create_tag(article)
        tag2 = test_utils.create_tag(article)
        response = test_utils.request_article(self.client, article)
        tags = response.context[-1]["article"].tag_set.all()
        self.assertEqual(tag1, tags[0])
        self.assertEqual(tag2, tags[1])

    def test_tags_displayed(self):
        article = test_utils.create_article()
        tag = test_utils.create_tag(article)
        response = test_utils.request_article(self.client, article)
        self.assertIn(tag.content, response.content)

    def test_tag_has_link_to_blog_search(self):
        article = test_utils.create_article()
        tag = test_utils.create_tag(article)
        response = test_utils.request_article(self.client, article)
        link = "{}?tags={}".format(reverse("blog_search"), tag.content)
        self.assertIn(link, response.content)

    def test_blog_tags(self):
        tag1 = test_utils.create_tag()
        tag2 = test_utils.create_tag()
        test_utils.create_tag(content=tag2.content)
        response = self.client.get(reverse("blog_tags"))
        tags = response.context[-1]["tags"]
        tag1 = {"content": tag1.content, "priority": 1}
        tag2 = {"content": tag2.content, "priority": 2}
        # The order is randomed.
        try:
            self.assertEqual(tags, [tag1, tag2])
        except AssertionError:
            self.assertEqual(tags, [tag2, tag1])

    def test_drafts_excluded(self):
        article = test_utils.create_article(is_draft=True)
        test_utils.create_tag(article)
        response = self.client.get(reverse("blog_tags"))
        tags = response.context[-1]["tags"]
        self.assertEqual(0, len(tags))


class SearchTest(TestCase):
    def test_no_results(self):
        response = self.client.get(reverse("blog_search"), {"phrase": test_utils.get_data()})
        found_articles = response.context[-1]["found_articles"]
        self.assertFalse(found_articles)
        test_utils.create_article()
        response = self.client.get(reverse("blog_search"), {"phrase": test_utils.get_data()})
        found_articles = response.context[-1]["found_articles"]
        self.assertFalse(list(found_articles))

    def test_by_phrase_in_article_title(self):
        article = test_utils.create_article(title="Spam and Eggs")
        response = self.client.get(reverse("blog_search"), {"phrase": "eggs"})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article])

    def test_by_phrase_in_article_content(self):
        article = test_utils.create_article(content="The quick brown fox jumps over the lazy dog.")
        response = self.client.get(reverse("blog_search"), {"phrase": "lazy dog"})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article])

    def test_many_results(self):
        article1 = test_utils.create_article(title="Spam and Eggs")
        article2 = test_utils.create_article(content="Spam, spam, spam, spam, spam...")
        response = self.client.get(reverse("blog_search"), {"phrase": "spam"})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article1, article2])

    def test_many_results_but_only_one_match(self):
        article1 = test_utils.create_article(title="Spam and Eggs")
        test_utils.create_article(content="Spam, spam, spam, spam, spam...")
        response = self.client.get(reverse("blog_search"), {"phrase": "eggs"})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article1])

    def test_by_tag(self):
        article = test_utils.create_article()
        tag = test_utils.create_tag(article, content="spam")
        response = self.client.get(reverse("blog_search"), {"tags": tag.content})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article])

    def test_by_tags(self):
        article = test_utils.create_article()
        tag1 = test_utils.create_tag(article, content="spam")
        tag2 = test_utils.create_tag(article, content="eggs")
        tags = "{},{}".format(tag1.content, tag2.content)
        response = self.client.get(reverse("blog_search"), {"tags": tags})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article])

    def test_by_phrase_with_regex(self):
        article = test_utils.create_article(content="Tip #42")
        response = self.client.get(reverse("blog_search"), {"phrase": r"#(\d)+"})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article])

    def test_by_phrase_and_tags(self):
        article_content = "spam"
        tag_content1 = "eggs"
        tag_content2 = "cheese"
        article1 = test_utils.create_article(content=article_content)
        article2 = test_utils.create_article(content=article_content)
        test_utils.create_tag(article1, content=tag_content1)
        test_utils.create_tag(article2, content=tag_content1)
        test_utils.create_tag(article2, content=tag_content2)
        response = self.client.get(reverse("blog_search"), {
            "phrase": article_content,
            "tags": "{}, {}".format(tag_content1, tag_content2)
        })
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [article2])

    def test_drafts_excluded(self):
        article = test_utils.create_article(is_draft=True)
        response = self.client.get(reverse("blog_search"), {"phrase": article.title})
        found_articles = response.context[-1]["found_articles"]
        self.assertEqual(list(found_articles), [])
