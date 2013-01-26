import math

from django import template


register = template.Library()


@register.filter
def max_priority(tags):
    return max(tags.values())


@register.filter
def css_class(max_priority, priority):
    classes = ["tag_size1", "tag_size2", "tag_size3", "tag_size4", "tag_size5", "tag_size6"]
    index = int(math.floor((priority / float(max_priority)) * len(classes))) - 1
    return classes[index]
