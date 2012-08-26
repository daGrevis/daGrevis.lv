from django.conf.urls import patterns, url

urlpatterns = patterns("user.views",
    url(r"^login/$", "login", name="user_login"),
)
