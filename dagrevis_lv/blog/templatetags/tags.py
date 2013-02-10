import math

from django import template


register = template.Library()


@register.filter
def get_style(tags, priority):
    max_priority = max(tags, key=lambda tag: tag["priority"])["priority"]
    size = max_priority / 10. * priority
    return "font-size: {}em;".format(size)
