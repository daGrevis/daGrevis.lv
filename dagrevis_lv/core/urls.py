from django.conf.urls import patterns, url


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
