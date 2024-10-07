import random

from colorama import Fore, Style, init
from django import template
from slugify import slugify

init()
register = template.Library()


@register.filter
def split_and_get_one(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]

    php_images = [url for url in urls if url.endswith('.php')]
    if php_images:
        return php_images[0]  # Возвращаем только первое изображение

    return urls[0] if urls else ''


@register.filter
def split_and_get_all(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]

    php_images = [url for url in urls if url.endswith('.php')]
    if php_images:
        return php_images[:1]

    return [urls[0], urls[1]]


@register.filter
def calculate_discount(price, discount):
    """Рассчитать цену со скидкой и сумму скидки"""
    try:
        final_price = price * (1 - float(discount) / 100)

        discount_amount = price * (float(discount) / 100)

        # Форматируем итоговую цену и сумму скидки
        formatted_final_price = '{:,.0f}'.format(final_price).replace(',', ' ')
        formatted_discount_amount = '{:,.0f}'.format(discount_amount).replace(',', ' ')

        return {
            'final_price': formatted_final_price,
            'discount_amount': formatted_discount_amount,
        }
    except (ValueError, TypeError) as e:
        print(f'Error in calculating discount: {e}')
        return {
            'final_price': price,
            'discount_amount': 0,
        }


@register.filter
def format_number(value):
    """Форматировать число с разделителями тысяч в виде пробелов"""
    try:
        value = float(value)
        formatted_value = '{:,.0f}'.format(value).replace(',', ' ')
        return formatted_value
    except (ValueError, TypeError):
        return value


@register.filter
def translit_slugify(value):
    return slugify(value)


@register.filter
def divisibleby(value, divisor):
    """Returns True if value is divisible by divisor, else False."""
    try:
        return value // divisor
    except (ValueError, TypeError):
        return False


@register.filter
def random_bg_with_text_color(value):
    bg_colors = [
        'bg-primary', 'bg-success', 'bg-danger',
        'bg-warning', 'bg-info', 'bg-secondary',
        'bg-light', 'bg-dark'
    ]

    chosen_bg = random.choice(bg_colors)

    if chosen_bg in [
        'bg-dark',
        'bg-primary',
        'bg-danger',
        'bg-secondary',
        'bg-success'
    ]:
        text_color = 'text-light'
    else:
        text_color = 'text-dark'

    return f"{chosen_bg} {text_color}"
