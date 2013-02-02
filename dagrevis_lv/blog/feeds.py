from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext

from blog.models import Article, Comment


class ArticlesFeed(Feed):
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


class CommentsFeed(Feed):
    def title(self):
        return settings.TITLE_FOR_COMMENTS_FEED

    def description(self):
        return settings.DESCRIPTION_FOR_COMMENTS_FEED

    def link(self):
        return settings.LINK_FOR_COMMENTS_FEED

    def items(self):
        return Comment.objects.all()[:settings.ITEM_LIMIT_FOR_COMMENTS_FEED]

    def item_title(self, comment):
        author = comment.author
        title = ugettext("Comment #{pk} by {username}").format(pk=comment.pk, username=author.username)
        return title

    def item_description(self, comment):
        return comment.content

    def item_link(self, comment):
        return comment.get_absolute_url()
