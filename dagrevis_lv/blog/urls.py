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
        r"^blog/(?P<article_pk>\d+)/(?P<slug>[a-z0-9-]+)/$",
        "article",
        name="blog_article",
    ),
    url(
        r"^blog/(?P<article_pk>\d+)/$",
        "article",
        name="blog_article",
    ),
    url(
        r"^blog/tags/$",
        "tags",
        name="blog_tags",
    ),
    url(
        r"^blog/search/$",
        "search",
        name="blog_search",
    ),
    url(
        r"^blog/articles_feed\.rss$",
        ArticlesRssFeed(),
        name="blog_articles_rss_feed",
    ),
    url(
        r"^blog/articles_feed\.atom$",
        ArticlesAtomFeed(),
        name="blog_articles_atom_feed",
    ),
    url(
        r"^blog/comments_feed\.rss$",
        CommentsRssFeed(),
        name="blog_comments_rss_feed",
    ),
    url(
        r"^blog/comments_feed\.atom$",
        CommentsAtomFeed(),
        name="blog_comments_atom_feed",
    ),
)
