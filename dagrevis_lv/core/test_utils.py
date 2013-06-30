"""
Test utilities are NOT tested because they are used by many tests and that's
why they are self-tested in indirect way.
"""

from uuid import uuid4

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from blog.models import Article, Comment, Tag


def get_data(length=32):
    """Get data for testing purposes."""
    data = ""
    while len(data) < length:
        data += str(uuid4())
    data = data[:length]
    return data


def create_user(username=None, password=None):
    username = username if username is not None else get_data()
    password = password if password is not None else get_data()
    return User.objects.create_user(username=username, password=password)


def create_and_login_user(client, username=None, password=None):
    """
    Store or genarate and then store the password, because it will be needed
    as plain text to login.
    """
    password = password if password is not None else get_data()
    user = create_user(username, password)
    client.login(username=user.username, password=password)


def logged_in(client):
    #TODO: Does it need to be hard-coded?
    return "_auth_user_id" in client.session


def create_article(author=None, created=None, title=None, content=None,
                   slug=None, tweet_id=None, is_draft=None):
    article = Article()
    article.author = author if author is not None else create_user()
    if created:
        article.created = created
    article.title = title if title is not None else get_data()
    article.content = content if content is not None else get_data()
    article.slug = slug if slug is not None else slugify(get_data())
    if tweet_id:
        article.tweet_id = tweet_id
    article.is_draft = is_draft if is_draft is not None else False
    article.save()
    return article


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


def create_tag(article=None, content=None):
    article = article if article is not None else create_article()
    content = content if content is not None else get_data()
    return Tag.objects.create(
        content=content,
        article=article,
    )


def request_article(client, article=None):
    article = article if article is not None else create_article()
    return client.get(article.get_absolute_url())
