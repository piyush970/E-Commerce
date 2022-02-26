from django import template

register = template.Library()

@register.filter(name='in_cart')
def in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;

@register.filter(name='total')
def total(product, cart):
    return product.discount_price * cart_quantity(product, cart)

@register.filter(name='cart_total')
def cart_total(products, cart):
    sum = 0;
    for p in products:
        sum += total(p, cart)
    return sum

@register.filter(name='quantity_total')
def quantity_total(products, cart):
    sum = 0;
    for p in products:
        sum += cart_quantity(p, cart)
    return sum
