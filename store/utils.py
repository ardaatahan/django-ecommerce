import json

from .models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'get_cart_items': 0,
        'get_cart_total': 0,
        'is_shipping': False
    }
    cart_items = order['get_cart_items']

    for id in cart:
        try:
            cart_items += cart[id]['quantity']

            product = Product.objects.get(pk=id)
            total = (product.price * cart[id]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[id]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'get_image_url': product.get_image_url
                },
                'quantity': cart[id]['quantity'],
                'get_total': total
            }

            items.append(item)

            if not product.digital:
                order['is_shipping'] = True
        except:
            pass

    return {
        'cart_items': cart_items,
        'order': order,
        'items': items
    }


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']

    return {
        'cart_items': cart_items,
        'order': order,
        'items': items
    }
    
