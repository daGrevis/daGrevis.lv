from django.conf.urls import patterns, url

from blog.sitemaps import ArticlesSitemap, PagesSitemap


urlpatterns = patterns(
    "core.views",
    url(
        r"^about/$",
        "about",
        name="core_about",
    ),
    url(
        r"^contacts/$",
        "contacts",
        name="core_contacts",
    ),
)

urlpatterns += patterns(
    "",
    url(
        r"^sitemap\.xml$",
        "django.contrib.sitemaps.views.sitemap",
        {
            "sitemaps": {
                "articles": ArticlesSitemap(),
                "pages": PagesSitemap(),
            }
        },
        name="core_sitemap",
    ),
)
