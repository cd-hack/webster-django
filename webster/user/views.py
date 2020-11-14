from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from client.models import Website, Product, Profile, Category
from user.models import Wishlist, CartProduct, Rating, Order, OrderProduct
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .decorators import *


def userLogin(request, storename):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return redirect(reverse('user:home', args=[storename]))
        else:
            messages.info(request, 'Username or Password is Wrong')
    context = {}
    return render(request, 'user/login.html')


def userRegister(request, storename):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        name = request.POST.get('name')
        try:
            a = Profile.objects.create_user(
                email=email, name=name, phone=phone, is_user=True, is_client=False, password=password)
            messages.info(request, "User Created! Now Login")
        except IntegrityError as e:
            messages.info(request, 'Username already exist! Try login')
            return redirect(reverse('user:register', args=[storename]))
        return redirect(reverse('user:login', args=[storename]))
    return render(request, 'user/register.html')


def userLogout(request, storename):
    logout(request)
    return redirect('user:shop', storename=storename)


def home(request, storename):
    website = get_object_or_404(Website, title=storename)
    categories = website.category_set.all()
    category1 = categories[0].product_set.all()[:4]
    category2 = categories[1].product_set.all()[:4]
    category3 = categories[2].product_set.all()[:4]
    context = {'storename': storename,
               'website': website, 'categories': categories, 'category_wise_lists': [category1,  category2, category3]}
    return render(request, 'user/index.html', context)


def shop(request, storename):
    website = get_object_or_404(Website, title=storename)
    #print("This is", website)
    products = Product.objects.filter(website=website)
    print(products)
    context = {'storename': storename, 'products': products}
    return render(request, 'user/shop.html', context)


def shop_by_category(request, storename, category):
    website = get_object_or_404(Website, title=storename)
    #category= Category.objects.filter(name=category,website=website)[0]
    products = Product.objects.filter(website=website)
    print(products)
    context = {'storename': storename, 'products': products}
    return render(request, 'user/shop.html', context)


def about(request, storename):
    context = {'storename': storename}
    return render(request, 'user/about.html', context)


def contact(request, storename):
    context = {'storename': storename}
    return render(request, 'user/contact.html', context)


def product_details(request, storename, id):
    product = Product.objects.get(id=id)
    ratings = Rating.objects.filter(product=product)
    context = {'storename': storename, 'product': product, 'ratings': ratings}
    return render(request, 'user/product-details.html', context)


@have_bought
def write_review(request, storename, id):
    product = Product.objects.get(id=id)
    context = {'storename': storename}
    if(request.method == 'POST'):
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        rating_obj = Rating(userprofile=request.user,
                            product=product, rating=rating, review=review)
        rating_obj.save()
        messages.info(request,'Review Added Successfully')
        return redirect('user:product-details', storename=storename, id=id)
    return render(request, 'user/add-review.html', context)


@is_authenticatd_user
def wishlist(request, storename):
    # print(request.user.is_user)
    profile = request.user
    website = Website.objects.get(title=storename)
    wishlists = profile.wishlist_set.filter(product__website=website)
    # print(wishlists[0].product.website)
    context = {'wishlists': wishlists, 'storename': storename}
    return render(request, 'user/wishlist.html', context)


@is_authenticatd_user
def cart(request, storename):
    profile = request.user
    website = Website.objects.get(title=storename)
    cart = profile.cartproduct_set.filter(product__website=website)
    grand_total = 0
    for item in cart:
        grand_total += item.total
    context = {'cart': cart, 'storename': storename,
               'grand_total': grand_total}
    return render(request, 'user/cart.html', context)


@is_authenticatd_user
def checkout(request, storename):
    context = {'storename': storename}
    if request.method == 'POST':
        cart_products = CartProduct.objects.filter(user=request.user)
        order_obj = Order.objects.create(
            user=request.user, website=Website.objects.get(title=storename))
        for cart_product in cart_products:
            order_product = OrderProduct.objects.create(
                quantity=cart_product.quantity, product=cart_product.product, total=cart_product.total, order=order_obj)
            cart_product.delete()
        return redirect('user:home', storename=storename)
    return render(request, 'user/confirm-order.html', context)


@is_authenticatd_user
def add_to_cart(request, storename, id):
    product = Product.objects.get(id=id)
    cart_item = CartProduct(
        user=request.user, quantity=1, product=product, total=500)
    cart_item.save()
    messages.info(request, 'Added To Cart')
    return redirect(reverse('user:cart', args=[storename]))


@is_authenticatd_user
def remove_from_cart(request, storename, id):
    cart_item = CartProduct.objects.get(id=id)
    cart_item.delete()
    messages.info(request, 'Removed From Cart')
    return redirect(reverse('user:cart', args=[storename]))


@is_authenticatd_user
def add_to_wishlist(request, storename, id):
    product = Product.objects.get(id=id)
    wishlist_item = Wishlist(
        userprofile=request.user,  product=product)
    wishlist_item.save()
    messages.info(request, 'Added To WishList')
    return redirect(reverse('user:shop', args=[storename]))


@is_authenticatd_user
def remove_from_wishlist(request, storename, id):
    wishlist_item = Wishlist.objects.get(id=id)
    wishlist_item.delete()
    messages.info(request, 'Removed From WishList')
    return redirect(reverse('user:wishlist', args=[storename]))
