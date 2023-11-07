from django import template
from datetime import datetime

register = template.Library()

@register.filter
def custom_date_format(value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return value.strftime("%d-%m-%Y")