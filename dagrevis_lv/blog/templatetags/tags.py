from django import template


register = template.Library()


@register.filter
def get_style(tags, priority):
    max_priority = max(tags, key=lambda tag: tag["priority"])["priority"]
    size = 100 / max_priority / priority / 2
    return "font-size: {}em;".format(size)
