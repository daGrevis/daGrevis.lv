from markdown2 import markdown as markdown_processor

from django import template
from django.utils import html, safestring
from django.template import defaultfilters


register = template.Library()


@register.filter(needs_autoescape=True)
@defaultfilters.stringfilter
def markdown(value, autoescape=None):
    """Escapes input and processes it with Markdown."""
    escaped_value = html.escape(value)
    generated_html = markdown_processor(escaped_value)
    return safestring.mark_safe(generated_html)
