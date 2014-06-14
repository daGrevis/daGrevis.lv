from django import template
from django.conf import settings


register = template.Library()


@register.filter
def get_style(tags, priority):
    max_priority = max(tags, key=lambda tag: tag["priority"])["priority"]
    size = ((max_priority / settings.RATIO_FOR_TAG_SIZE)
            - (100 / max_priority / priority / settings.RATIO_FOR_TAG_SIZE))
    return "font-size: {}em;".format(size)
