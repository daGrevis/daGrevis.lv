# Test utilities.

from uuid import uuid4
from django.contrib.auth.models import User
from blog.models import *
from django.template import defaultfilters


def create_user(username=None, password=None):
    username = username if username is not None else str(uuid4())
    password = password if password is not None else str(uuid4())
    return User.objects.create_user(username=username, password=password)


def create_article(user=None, title=None, content=None, slug=None):
    user = user if user is not None else create_user()
    title = title if title is not None else str(uuid4())
    content = content if content is not None else str(uuid4())
    slug = slug if slug is not None else defaultfilters.slugify(str(uuid4()))
    return Article.objects.create(
        user=user,
        title=title,
        content=content,
        slug=slug,
    )


def logged_in(client):
    return "_auth_user_id" in client.session
