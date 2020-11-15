from django.http import HttpResponse
from client.models import Website, Product, Profile
from django.shortcuts import redirect
from django.contrib import messages


def is_authenticatd_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('user:login', storename=kwargs['storename'])
    return wrapper_func


def have_bought(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if Product.objects.get(id=kwargs['id']).orderproduct_set.filter(order__user=request.user):
                return view_func(request, *args, **kwargs)
            messages.info(request, 'You have not purchased this product')
            return redirect('user:product-details', storename=kwargs['storename'], id=kwargs['id'])
    return wrapper_func
