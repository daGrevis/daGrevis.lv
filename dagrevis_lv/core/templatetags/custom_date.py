from datetime import date

from django import template


register = template.Library()


@register.filter
def fake_date_without_day(value):
    """Fakes `date`. Sets day to `1`."""
    return date(year=value[0], month=value[1], day=1)
