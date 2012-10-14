from django.conf.urls import patterns, url


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
)
