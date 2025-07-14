from django import template
register = template.Library()

@register.filter
def safe_get(d, key):
    if isinstance(d, dict):
        return d.get(key, None)
    return None
