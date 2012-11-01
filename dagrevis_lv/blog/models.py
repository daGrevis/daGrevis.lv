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
    depth = 1

    def __unicode__(self):
        return self.content

    @staticmethod
    def calculate_depth_and_sort(comments, sorted_comments=None, deeper_comment=None, depth=0):
        """
        @brief Calculates depth of comments and sorts them. Uses recursion, be careful!
        @param comments: Comments (unsorted)
        @param sorted_comments: Sorted comments (for recursion, isn't used from outside)
        @param deeper_comment: Comment that is deeper than current comment (for recursion, isn't used from outside)
        @param depth: Depth (for recursion, isn't used from outside)
        @return Sorted comments w/ depth
        """
        for comment in comments:
            if comment.parent == deeper_comment:
                comment.depth = depth
                if sorted_comments is None:
                    sorted_comments = []
                sorted_comments.append(comment)
                Comment.calculate_depth_and_sort(comments, sorted_comments, comment, depth + 1)
        return sorted_comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )
