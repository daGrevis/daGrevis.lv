from django.conf.urls import patterns, url


urlpatterns = patterns(
    "user.views",
)

urlpatterns += patterns(
    "",
    url(r"^user/login/$", "django.contrib.auth.views.login", {"template_name": "login.html"}, name="user_login"),
)
