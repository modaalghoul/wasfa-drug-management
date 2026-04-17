from django import template
from django.urls import translate_url

register = template.Library()

@register.simple_tag(takes_context=True)
def change_language(context, language):
    """
    Generate a URL to switch language
    """
    request = context['request']
    path = request.path
    return translate_url(path, language)
