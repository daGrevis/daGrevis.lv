from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.core.urlresolvers import reverse

from blog.models import Article


class ArticlesSitemap(Sitemap):
    def items(self):
        return (Article.objects
                .order_by("-pk")[:settings.ARTICLES_SITEMAP["ITEM_LIMIT"]])

    def location(self, article):
        return article.get_absolute_url()

    def lastmod(self, article):
        if article.modified:
            return article.modified

    def changefreq(self, article):
        return settings.ARTICLES_SITEMAP["CHANGEFREQ"]

    def priority(self, article):
        return settings.ARTICLES_SITEMAP["PRIORITY"]


class Page(object):
    def __init__(self, url):
        self.url = reverse(url)


class PagesSitemap(Sitemap):
    def items(self):
        return [Page(page) for page in settings.PAGES]

    def location(self, page):
        return page.url

    def changefreq(self, article):
        return settings.PAGES_SITEMAP["CHANGEFREQ"]

    def priority(self, article):
        return settings.PAGES_SITEMAP["PRIORITY"]
