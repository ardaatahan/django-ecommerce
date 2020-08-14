from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from datetime import datetime
import json

from .models import *
from .utils import *

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store"))
        else:
            return render(request, "store/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("store"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "store/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            customer = Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )
        except IntegrityError:
            return render(request, "store/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("store"))
    else:
        return render(request, "store/register.html")


def store(request):

    # Get the customer, order, and items depending on the user authentication
    data = cart_data(request)
    cart_items = data['cart_items']
    
    # Get the products
    products = Product.objects.all()
    return render(request, 'store/store.html', {
        'products': products,
        'cart_items': cart_items
    })


def cart(request):

    # Get the customer, order, and items depending on the user authentication
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    return render(request, 'store/cart.html', {
        'items': items,
        'order': order,
        'cart_items': cart_items
    })


def checkout(request):

    # Get the customer, order, and items depending on the user authentication
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

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

    # Process the order for an authenticated user
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    # Process the order for an unauthenticated user
    else:
        name = data['form']['name']
        email = data['form']['email']

        cookie_data = cookie_cart(request)
        items = cookie_data['items']

        customer, created = Customer.object.get_or_create(email=email)
        customer.name = name

        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False
        )

        for item in items:
            product = Product.object.get(pk=item['product']['id'])

            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

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
