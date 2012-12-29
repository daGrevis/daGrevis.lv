from django import forms
from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


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

    def tags(self):
        return self.tag_set.all()

    def get_link(self):
        return reverse("blog_article", kwargs={"article_pk": self.pk, "slug": self.slug})


class Comment(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True)
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content = models.TextField()
    depth = None

    def __unicode__(self):
        return self.content

    @staticmethod
    def calculate_depth_and_sort(comments, _sorted_comments=None, _deeper_comment=None, _depth=1):
        """
        @brief Calculates depth of comments and sorts them.
        @param comments: Comments (unsorted).
        @param _sorted_comments: Sorted comments (for recursion, isn't used from outside).
        @param _deeper_comment: Comment that is deeper than current comment (for recursion, isn't used from outside).
        @param _depth: Depth (for recursion, isn't used from outside).
        @return Sorted comments w/ depth.
        """
        for comment in comments:
            if comment.parent == _deeper_comment:
                comment.depth = _depth
                if _sorted_comments is None:
                    _sorted_comments = []
                _sorted_comments.append(comment)
                Comment.calculate_depth_and_sort(comments, _sorted_comments, comment, _depth + 1)
        return _sorted_comments

    def get_depth(self):
        """Calculates depth. **Will perform one query for each level, be careful!"""
        depth = 1
        comment = self
        while comment.parent is not None:
            depth += 1
            comment = comment.parent
        return depth


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )


class Tag(models.Model):
    article = models.ForeignKey(Article)
    content = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content
