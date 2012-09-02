from django import template
import markdown2

register = template.Library()


@register.filter
def eggs(value):
    return value
