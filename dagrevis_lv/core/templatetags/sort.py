from django import template


register = template.Library()


@register.filter
def dict_reverse(value):
    for key in sorted(value.keys(), reverse=True):
        yield key, value[key]
