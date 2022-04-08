from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import JsonResponse
import json
from datetime import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    category = request.GET.get('category')

    if category is None:
        products = Product.objects.order_by('-created_at')
    else:
        products = Product.objects.filter(category__name=category)

    page_num = request.GET.get("page")
    paginator = Paginator(products, 6)

    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'categories': categories,
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer
    print(customer)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = int(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            phoneNumber=data['shipping']['phoneNumber'],
            fullname=data['shipping']['fullname'],
            region=data['shipping']['region'],
            city=data['shipping']['city'],
            neighborhood=data['shipping']['neighborhood'],
            company_name=data['shipping']['company_name'],
            additional=data['shipping']['additional'],
        )

    return JsonResponse('Payment complete', safe=False)