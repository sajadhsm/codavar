from datetime import timedelta

from django import template

register = template.Library()

@register.filter
def timedelta_hide_seconds(time):
    return ':'.join(str(time).split(':')[:2])