from django import template

register = template.Library()


@register.filter
def split_and_get_first_two(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]
    return urls[:2]
