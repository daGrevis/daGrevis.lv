from os import path


DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = "x" * 32

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

DATABASE_ROUTERS = [
    "core.routers.DefaultRouter",
    "legacy.routers.LegacyRouter",
]

TIME_ZONE = "Europe/Riga"

LANGUAGE_CODE = "lv"

SITE_ID = 1

STATIC_ROOT = path.join(path.dirname(__file__), "static")

STATIC_URL = "/static/"

ROOT_URLCONF = "dagrevis_lv.urls"

WSGI_APPLICATION = "dagrevis_lv.wsgi.application"

TEMPLATE_DIRS = (
    path.join(path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.admin",
    "social_auth",
    "gunicorn",
    "south",
    "core",
    "blog",
    "user",
    "legacy",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "core.context_processors.settings",
)

MAX_DEPTH_FOR_COMMENT = 5

SITE_TITLE = "daGrevis.lv"
META_DESCRIPTION = ""
META_AUTHOR = ""
AUTHOR_NAME = "Raitis (daGrevis) Stengrevics"
AUTHOR_URL = "/about/"

GA_ENABLED = False
GA_ID = "UA-7141181-6"

ARTICLE_COUNT_PER_PAGE = 20
TAG_COUNT_IN_TAG_CLOUD = 40

ARTICLES_FEED = {
    "RSS_TITLE": "Articles feed (RSS)",
    "ATOM_TITLE": "Articles feed (Atom)",
    "DESCRIPTION": "Latest articles",
    "RSS_LINK": "blog_articles_rss_feed",
    "ATOM_LINK": "blog_articles_atom_feed",
    "ITEM_LIMIT": 5,
}

COMMENTS_FEED = {
    "RSS_TITLE": "Comments feed (RSS)",
    "ATOM_TITLE": "Comments feed (Atom)",
    "DESCRIPTION": "Latest comments",
    "RSS_LINK": "blog_comments_rss_feed",
    "ATOM_LINK": "blog_comments_atom_feed",
    "ITEM_LIMIT": 20,
}

ARTICLES_SITEMAP = {
    "ITEM_LIMIT": ARTICLE_COUNT_PER_PAGE,
    "CHANGEFREQ": "always",
    "PRIORITY": 1.,
}

PAGES_SITEMAP = {
    "CHANGEFREQ": "never",
    "PRIORITY": .5,
}

PAGES = [
    "blog_articles",
    "core_about",
    "core_contacts",
    "blog_tags",
    "blog_search",
    "blog_articles_rss_feed",
    "blog_articles_atom_feed",
    "blog_comments_rss_feed",
    "blog_comments_atom_feed",
]

CONTENTS_OF_ROBOTS_TXT = (
    "User-agent: *\n"
    "Disallow: /admin/\n"
    "Sitemap: /sitemap.xml"
)

CONTENTS_OF_HUMANS_TXT = (
    "Coded and designed by Raitis (daGrevis) Stengrevics."
)

AUTHENTICATION_BACKENDS = (
    "social_auth.backends.twitter.TwitterBackend",
    "social_auth.backends.contrib.github.GithubBackend",
    "django.contrib.auth.backends.ModelBackend",
)

TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""

GITHUB_APP_ID = ""
GITHUB_API_SECRET = ""

SOCIAL_AUTH_EXTRA_DATA = False

LOGIN_REDIRECT_URL = "/"

URL_TO_TWITTER_TWEET = "https://twitter.com/daGrevis_lv/status/{}"
