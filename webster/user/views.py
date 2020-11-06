from django.shortcuts import render

# Create your views here.


def home(request, storename):
    
    return render(request, 'user/index.html')


def shop(request, storename):
    return render(request, 'user/shop.html')


def about(request, storename):
    return render(request, 'user/about.html')


def contact(request, storename):
    return render(request, 'user/contact.html')


def product_details(request, storename, id):
    return render(request, 'user/product-details.html')


def wishlist(request, storename):
    return render(request, 'user/wishlist.html')

def cart(request, storename):
    return render(request, 'user/cart.html')

def checkout(request, storename):
    return render(request, 'user/checkout.html')


