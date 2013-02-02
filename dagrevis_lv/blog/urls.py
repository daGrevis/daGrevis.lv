from django.conf.urls import patterns, url
from blog.feeds import ArticlesFeed, CommentsFeed


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
        r"^articles_feed/$",
        ArticlesFeed(),
        name="blog_articles_feed",
    ),
    url(
        r"^comments_feed/$",
        CommentsFeed(),
        name="blog_comments_feed",
    ),
)
