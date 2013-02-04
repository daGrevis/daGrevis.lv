from django.contrib import admin
from django.conf.urls import patterns, include, url


admin.autodiscover()

urlpatterns = patterns(
    "",
    url(r"^admin/", include(admin.site.urls)),
    url(r"", include("social_auth.urls")),
    url(r"^", include("core.urls")),
    url(r"^", include("blog.urls")),
    url(r"^", include("user.urls")),
    url(r"^", include("legacy.urls")),
)
