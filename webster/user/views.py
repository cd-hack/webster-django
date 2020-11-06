from django.shortcuts import render

# Create your views here.


def home(request, storename):
    return render(request, 'user/index.html')


def shop(request, storename):
    return render(request, 'user/shop.html')