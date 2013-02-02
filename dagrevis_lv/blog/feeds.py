from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext
from django.utils.feedgenerator import Atom1Feed

from blog.models import Article, Comment


class ArticlesRssFeed(Feed):
    def title(self):
        return settings.TITLE_FOR_ARTICLES_FEED

    def description(self):
        return settings.DESCRIPTION_FOR_ARTICLES_FEED

    def link(self):
        return settings.LINK_FOR_ARTICLES_FEED

    def items(self):
        return Article.objects.order_by("-pk")[:settings.ITEM_LIMIT_FOR_ARTICLES_FEED]

    def item_title(self, article):
        return article.title

    def item_description(self, article):
        return article.content

    def item_link(self, article):
        return article.get_absolute_url()


class ArticlesAtomFeed(ArticlesRssFeed):
    feed_type = Atom1Feed
    subtitle = ArticlesRssFeed.description


class CommentsRssFeed(Feed):
    def title(self):
        return settings.TITLE_FOR_COMMENTS_FEED

    def description(self):
        return settings.DESCRIPTION_FOR_COMMENTS_FEED

    def link(self):
        return settings.LINK_FOR_COMMENTS_FEED

    def items(self):
        return Comment.objects.order_by("-pk")[:settings.ITEM_LIMIT_FOR_COMMENTS_FEED]

    def item_title(self, comment):
        author = comment.author
        title = ugettext("Comment #{pk} by {username}").format(pk=comment.pk, username=author.username)
        return title

    def item_description(self, comment):
        return comment.content

    def item_link(self, comment):
        return comment.get_absolute_url()


class CommentsAtomFeed(CommentsRssFeed):
    feed_type = Atom1Feed
    subtitle = CommentsRssFeed.description
