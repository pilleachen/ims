# your_app/templatetags/custom_tags.py
from django import template
from ..models import Subject

register = template.Library()

@register.filter
def get_item(value, arg):
    if arg == 'subject':
        return Subject.objects.get(id=value)
    return value
