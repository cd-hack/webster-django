from django.shortcuts import render, get_object_or_404
from client.models import Website, Product

# Create your views here.







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
    product= Product.objects.get(id=id)
    context = {'storename': storename,'product':product}
    return render(request, 'user/product-details.html', context)


def wishlist(request, storename):
    context = {'storename': storename}

    return render(request, 'user/wishlist.html', context)


def cart(request, storename):
    context = {'storename': storename}

    return render(request, 'user/cart.html', context)


def checkout(request, storename):
    context = {'storename': storename}

    return render(request, 'user/checkout.html', context)
