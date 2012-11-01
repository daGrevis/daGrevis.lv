from django import forms
from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User


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
    parent = models.ForeignKey("self", null=True, blank=True)
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content = models.TextField()
    depth_level = 1

    def __unicode__(self):
        return self.content

    @staticmethod
    def calculate_depth(comments, sorted_comments=None, comment=None, depth_level=1):
        """
        @brief Calculates depth of comments w/ recursion.
        @param comments: Comments
        @param comment: Comment (for recursion, isn't used from outside)
        @param depth_level: Depth level (for recursion, isn't used from outside)
        @return Comments /w depth level
        """
        for the_comment in comments:
            if the_comment.parent == comment:
                the_comment.depth_level = depth_level
                if sorted_comments is None:
                    sorted_comments = []
                sorted_comments.append(the_comment)
                Comment.calculate_depth(comments, sorted_comments, the_comment, depth_level + 1)
        return sorted_comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )
