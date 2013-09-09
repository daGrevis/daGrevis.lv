from django import template


register = template.Library()


@register.filter
def is_visible(comment, user):
    if not comment.article.is_comments_moderated:
        return True
    if comment.is_moderated:
        return True
    if comment.author == user:
        return True
