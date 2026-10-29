import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdownify(text):
    html = markdown.markdown(text, extensions=['fenced_code', 'codehilite', 'nl2br'])
    return mark_safe(html)