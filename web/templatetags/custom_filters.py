from django import template

register = template.Library()


@register.filter
def split_and_get_all(value):
    urls = [url.strip() for url in value.split(',') if url.strip()]
    return urls


@register.filter
def calculate_discount(price, discount):
    try:
        clean_price = float(price.replace(' ', ''))
        discount_value = float(discount) / 100
        final_price = clean_price * (1 - discount_value)
        formatted_price = '{:,.0f}'.format(final_price).replace(',', ' ')
        return formatted_price
    except (ValueError, TypeError) as e:
        print(f'Error in calculating discount: {e}')
        return price
