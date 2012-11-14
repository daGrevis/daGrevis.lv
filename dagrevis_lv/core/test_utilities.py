"""Test utilities are NOT tested because they are used by many tests and that's why they are self-tested in indirect way."""

import exceptions
from uuid import uuid4

from blog.models import Article, Comment
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


def get_data(unique=True, random=True, length=None):
    """Get data for testing purposes. By default data is unique and random."""
    if unique and random:
        data = str(uuid4())
        if length is not None:
            data = data[:length]
        return data
    else:
        raise exceptions.NotImplementedError


def create_user(username=None, password=None):
    username = username if username is not None else get_data()
    password = password if password is not None else get_data()
    return User.objects.create_user(username=username, password=password)


def create_and_login_user(client, username=None, password=None):
    # Store or genarate and then store the password, because it will be needed as plain text to login.
    password = password if password is not None else get_data()
    user = create_user(username, password)
    client.login(username=user.username, password=password)


def logged_in(client):
    #TODO: Does it need to be hard-coded?
    return "_auth_user_id" in client.session


def create_article(author=None, title=None, content=None, slug=None):
    author = author if author is not None else create_user()
    title = title if title is not None else get_data()
    content = content if content is not None else get_data()
    slug = slug if slug is not None else slugify(get_data())
    return Article.objects.create(
        author=author,
        title=title,
        content=content,
        slug=slug,
    )


def create_comment(article=None, author=None, content=None, parent=None):
    article = article if article is not None else create_article()
    author = author if author is not None else create_user()
    content = content if content is not None else get_data()
    return Comment.objects.create(
        parent=parent,
        article=article,
        author=author,
        content=content,
    )
