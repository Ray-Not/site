from django import template
from slugify import slugify

register = template.Library()


@register.filter
def split_and_get_all(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]
    return urls


@register.filter
def calculate_discount(price, discount):
    """Рассчитать цену со скидкой"""
    try:
        # Так как price теперь является числовым полем, преобразование не нужно
        final_price = price * (1 - float(discount) / 100)
        formatted_price = '{:,.0f}'.format(final_price).replace(',', ' ')
        return formatted_price
    except (ValueError, TypeError) as e:
        print(f'Error in calculating discount: {e}')
        return price


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
