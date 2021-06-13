from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter(name='reverse')
@stringfilter
def reverse(value):
    return value[::-1]

