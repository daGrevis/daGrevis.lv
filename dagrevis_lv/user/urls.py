from django.conf.urls import patterns, url


urlpatterns = patterns(
    "user.views",
    url(r"^user/registration/$", "registration", name="user_registration"),
    url(r"^user/logout/$", "logout", name="user_logout"),
)

urlpatterns += patterns(
    "",
    url(r"^user/login/$", "django.contrib.auth.views.login", {"template_name": "login.html"}, name="user_login"),
)
