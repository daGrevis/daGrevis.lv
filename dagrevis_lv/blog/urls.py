from django.conf.urls import patterns, url
from blog.feeds import ArticlesRssFeed, ArticlesAtomFeed, CommentsRssFeed, CommentsAtomFeed


urlpatterns = patterns(
    "blog.views",
    url(
        r"^$",
        "articles",
        name="blog_articles",
    ),
    url(
        r"^article/(?P<article_pk>\d+)/(?P<slug>[a-z0-9-]+)/$",
        "article",
        name="blog_article",
    ),
    url(
        r"^article/(?P<article_pk>\d+)/$",
        "article",
        name="blog_article",
    ),
    url(
        r"^tags/$",
        "tags",
        name="blog_tags",
    ),
    url(
        r"^search/$",
        "search",
        name="blog_search",
    ),
    url(
        r"^articles_feed\.rss$",
        ArticlesRssFeed(),
        name="blog_articles_rss_feed",
    ),
    url(
        r"^articles_feed\.atom$",
        ArticlesAtomFeed(),
        name="blog_articles_atom_feed",
    ),
    url(
        r"^comments_feed\.rss$",
        CommentsRssFeed(),
        name="blog_comments_rss_feed",
    ),
    url(
        r"^comments_feed\.atom$",
        CommentsAtomFeed(),
        name="blog_comments_atom_feed",
    ),
)
