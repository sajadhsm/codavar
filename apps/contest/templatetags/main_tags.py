from datetime import timedelta

from django import template

register = template.Library()

@register.filter
def timedelta_hide_seconds(time):
    return ':'.join(str(time).split(':')[:2])

@register.filter
def respective_bg_color_css_rule(sub):
    '''Give leaderboard submission cell background color'''
    opacity = sub.judge_score / sub.problem.score
    return 'background-color: rgba(41, 168, 71, {});'.format(opacity)