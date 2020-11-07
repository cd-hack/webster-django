from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from client.models import Website, Product
from user.models import Wishlist, CartProduct
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.


def userLogin(request, storename):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return redirect(reverse('user:home', args=['mycakestore']))
        else:
            messages.info(request, 'Username or Password is Wrong')
    context = {}
    return render(request, 'user/login.html')


def userRegister(request):
    pass


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
    print("This is", website)
    products = Product.objects.filter(website=website.id)
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
    context = {'storename': storename, 'product': product}
    return render(request, 'user/product-details.html', context)


def wishlist(request, storename):
    # print(request.user.is_user)
    profile = request.user
    website = Website.objects.get(title=storename)

    wishlists = profile.wishlist_set.filter(product__website=website)
    # print(wishlists[0].product.website)
    context = {'wishlists': wishlists, 'storename': storename}
    return render(request, 'user/wishlist.html', context)


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


def checkout(request, storename):
    context = {'storename': storename}
    return render(request, 'user/checkout.html', context)


def add_to_cart(request, storename, id):
    product = Product.objects.get(id=id)
    cart_item = CartProduct(
        user=request.user, quantity=1, product=product, total=500)
    cart_item.save()
    messages.info(request, 'Added To Cart')
    return redirect(reverse('user:shop', args=[storename]))


def remove_from_cart(request, storename, id):
    cart_item = CartProduct.objects.get(id=id)
    cart_item.delete()
    messages.info(request, 'Removed From Cart')
    return redirect(reverse('user:cart', args=[storename]))


def add_to_wishlist(request, storename, id):
    product = Product.objects.get(id=id)
    wishlist_item = Wishlist(
        userprofile=request.user,  product=product)
    wishlist_item.save()
    messages.info(request, 'Added To WishList')
    return redirect(reverse('user:shop', args=[storename]))


def remove_from_wishlist(request, storename, id):
    wishlist_item = Wishlist.objects.get(id=id)
    wishlist_item.delete()
    messages.info(request, 'Removed From WishList')
    return redirect(reverse('user:wishlist', args=[storename]))
