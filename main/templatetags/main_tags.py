from datetime import timedelta

from django import template

register = template.Library()

@register.filter
def timedelta_hh_mm(time):
    seconds = round(time.total_seconds())
    return str(timedelta(seconds=seconds))