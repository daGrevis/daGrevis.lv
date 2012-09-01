from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from django import forms


class Article(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title

    def clean(self):
        """Generates and saves slug, if it's not set."""
        if self.slug == "":
            self.slug = defaultfilters.slugify(self.title)
        super(Article, self).clean()


class Comment(models.Model):
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __unicode__(self):
        return self.content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )
