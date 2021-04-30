import datetime

from django import template

register = template.Library()


@register.filter
def plus_days(value, days):
    return value + datetime.timedelta(days=days)


@register.simple_tag
def current_date():
    return datetime.datetime.now().date()
