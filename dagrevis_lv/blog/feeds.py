from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse

from blog.models import Article, Comment


class ArticlesRssFeed(Feed):
    def title(self):
        return ugettext(settings.ARTICLES_FEED["RSS_TITLE"])

    def description(self):
        return ugettext(settings.ARTICLES_FEED["DESCRIPTION"])

    def link(self):
        return reverse(settings.ARTICLES_FEED["RSS_LINK"])

    def items(self):
        return (Article.objects.filter(is_draft=False).order_by("-pk")
                [:settings.ARTICLES_FEED["ITEM_LIMIT"]])

    def item_title(self, article):
        return article.title

    def item_description(self, article):
        return article.get_content_as_html()

    def item_link(self, article):
        return article.get_absolute_url()


class ArticlesAtomFeed(ArticlesRssFeed):
    feed_type = Atom1Feed
    subtitle = ArticlesRssFeed.description

    def title(self):
        return ugettext(settings.ARTICLES_FEED["ATOM_TITLE"])

    def link(self):
        return reverse(settings.ARTICLES_FEED["ATOM_LINK"])


class CommentsRssFeed(Feed):
    def title(self):
        return ugettext(settings.COMMENTS_FEED["RSS_TITLE"])

    def description(self):
        return ugettext(settings.COMMENTS_FEED["DESCRIPTION"])

    def link(self):
        return reverse(settings.COMMENTS_FEED["RSS_LINK"])

    def items(self):
        return (Comment.objects.filter(article__is_draft=False).order_by("-pk")
                [:settings.COMMENTS_FEED["ITEM_LIMIT"]])

    def item_title(self, comment):
        title = (ugettext("Comment #{pk} by {username}")
                 .format(pk=comment.pk, username=comment.author.username))
        return title

    def item_description(self, comment):
        return comment.get_content_as_html()

    def item_link(self, comment):
        return comment.get_absolute_url()


class CommentsAtomFeed(CommentsRssFeed):
    feed_type = Atom1Feed
    subtitle = CommentsRssFeed.description

    def title(self):
        return ugettext(settings.COMMENTS_FEED["ATOM_TITLE"])

    def link(self):
        return reverse(settings.COMMENTS_FEED["ATOM_LINK"])
