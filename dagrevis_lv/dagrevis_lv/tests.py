# Test utilities.

from uuid import uuid4
from django.contrib.auth.models import User
from blog.models import *
from django.template import defaultfilters


def create_user(username=None, password=None):
    username = username if username else str(uuid4())
    password = password if password else str(uuid4())
    user = User.objects.create_user(username=username, password=password)
    return user


def create_article(user=None, title=None, content=None, slug=None):
    user = user if user else create_user()
    title = title if title else str(uuid4())
    content = content if content else str(uuid4())
    slug = slug if slug else defaultfilters.slugify(str(uuid4()))
    article = Article()
    article.user = user
    article.title = title
    article.content = content
    article.slug = slug
    article.save()
    return article


def logged_in(client):
    return "_auth_user_id" in client.session
