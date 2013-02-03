from django.conf.urls import patterns, url


urlpatterns = patterns(
    "legacy.views",
    url(
        r"^article/(?P<article_pk>\d+)",
        "legacy_blog_article",
        name="legacy_blog_article",
    ),
)
