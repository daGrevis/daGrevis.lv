from django.conf.urls import patterns, url


urlpatterns = patterns(
    "user.views",
    url(r"^user/registration/$", "registration", name="user_registration"),
)

urlpatterns += patterns(
    "",
    url(r"^user/login/$", "django.contrib.auth.views.login", {"template_name": "login.html"}, name="user_login"),
    url(r"^user/logout/$", "django.contrib.auth.views.logout", name="user_logout"),
)
