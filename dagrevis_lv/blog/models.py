from datetime import datetime
from markdown import markdown

from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings


class Article(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(default=datetime.now)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(db_index=True)
    slug = models.CharField(max_length=255, blank=True)
    tweet_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def clean(self):
        """Generates and saves slug, if it's not set."""
        if self.slug == "":
            self.slug = defaultfilters.slugify(self.title)
        super(Article, self).clean()

    def get_absolute_url(self):
        return reverse("blog_article", kwargs={"article_pk": self.pk, "slug": self.slug})

    def get_content_as_html(self):
        return markdown(self.content, safe_mode="escape")

    def get_tweet_link(self):
        return "https://twitter.com/daGrevis_lv/status/{}".format(self.tweet_id)

    @staticmethod
    def sort_articles_by_month(articles):
        sorted_articles = {}
        for article in articles:
            created = article.created
            key = created.year, created.month
            if key not in sorted_articles:
                sorted_articles[key] = [article]
            else:
                sorted_articles[key].append(article)
        return sorted_articles

    @staticmethod
    def search_articles(phrase=None, tags=[]):
        """Searches for an articles by it's title and content, and / or tags. Results are "and'ed" together."""
        query_set = Article.objects.all()
        phrase_query = (models.Q(title__icontains=phrase)
                        | models.Q(content__icontains=phrase)
                        | models.Q(title__regex=phrase)
                        | models.Q(content__regex=phrase))
        if phrase:
            query_set = query_set.filter(phrase_query)
        if tags:
            query_set = (query_set
                         .filter(tag__content__in=tags)
                         .annotate(num_tags=models.Count("tag"))
                         .filter(num_tags=len(tags)))
        return query_set[:settings.ARTICLE_COUNT_PER_PAGE]


class Comment(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content = models.TextField(db_index=True)
    depth = None

    def __unicode__(self):
        return self.content

    def get_absolute_url(self):
        article = self.article
        before_hash = article.get_absolute_url()
        after_hash = "comment{}".format(self.pk)
        link = "{before_hash}#{after_hash}".format(before_hash=before_hash, after_hash=after_hash)
        return link

    def get_content_as_html(self):
        return markdown(self.content, safe_mode="escape")

    @staticmethod
    def calculate_depth_and_sort(comments, _sorted_comments=None, _deeper_comment=None, _depth=1):
        """
        @brief Calculates depth of comments and sorts them.
        @param comments: Comments (unsorted).
        @param _sorted_comments: Sorted comments (for recursion, isn't used from outside).
        @param _deeper_comment: Comment that is deeper than current comment (for recursion, isn't used from outside).
        @param _depth: Depth (for recursion, isn't used from outside).
        @return Sorted comments w/ depth.
        """
        for comment in comments:
            if comment.parent == _deeper_comment:
                comment.depth = _depth
                if _sorted_comments is None:
                    _sorted_comments = []
                _sorted_comments.append(comment)
                Comment.calculate_depth_and_sort(comments, _sorted_comments, comment, _depth + 1)
        return _sorted_comments

    def get_depth(self):
        """Calculates depth. **Will perform one query for each level, be careful!"""
        depth = 1
        comment = self
        while comment.parent is not None:
            depth += 1
            comment = comment.parent
        return depth


class Tag(models.Model):
    article = models.ForeignKey(Article)
    content = models.CharField(max_length=255, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

    @staticmethod
    def get_tags_by_priority():
        tags = Tag.objects.all()
        sorted_tags = {}
        for tag in tags:
            if tag.content in sorted_tags:
                sorted_tags[tag.content] += 1
            else:
                sorted_tags[tag.content] = 1
        return sorted_tags
