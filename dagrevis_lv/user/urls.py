from django.conf.urls import patterns, url


urlpatterns = patterns(
    "user.views",
    url(r"^user/registration/$", "registration", name="user_registration"),
    url(r"^user/login/$", "login", name="user_login"),
    url(r"^user/logout/$", "logout", name="user_logout"),
)
