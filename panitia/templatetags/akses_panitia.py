from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_panitia(context):
    user = context['user']
    return user.is_superuser or user.groups.filter(name='Panitia').exists()
