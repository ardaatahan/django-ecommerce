from django.shortcuts import render
from django.http import JsonResponse

from datetime import datetime
import json

from .models import *

# Create your views here.
def store(request):

    # Get the customer, order, and items depending on the user authentication
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
            'shipping': False 
        }
        cart_items = order['get_cart_items']

    # Get the products
    products = Product.objects.all()
    return render(request, 'store/store.html', {
        'products': products,
        'cart_items': cart_items
    })


def cart(request):

    # Get the customer, order, and items depending on the user authentication
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
            'shipping': False
        }
        cart_items = order['get_cart_items']

    return render(request, 'store/cart.html', {
        'items': items,
        'order': order,
        'cart_items': cart_items
    })


def checkout(request):

    # Get the customer, order, and items depending on the user authentication
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
            'shipping': False
        }
        cart_items = order['get_cart_items']

    return render(request, 'store/checkout.html', {
        'items': items,
        'order': order,
        'cart_items': cart_items
    })


def update_item(request):

    # Get the request body
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    # Get the customer and product
    customer = request.user.customer
    product = Product.objects.get(pk=product_id)

    # Create or get the order object if it exists
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Create an order item object
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Depending on the action add or remove the item
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    # Save the order item
    order_item.save()

    # If the order item quantity is less than 1 delete it
    if order_item.quantity < 1:
        order_item.delete()

    return JsonResponse('Item was added successfully.', safe=False)


def process_order(request):

    # Create a unique transaction id
    transaction_id = datetime.now().timestamp()

    # Get the sent data
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total']) 
        order.transaction_id = transaction_id

        if order.get_cart_total == total:
            order.complete = True
        
        order.save()

        if order.is_shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            ) 

    return JsonResponse('Payment complete.', safe=False)