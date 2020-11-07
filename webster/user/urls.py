from django.urls import path, include
from user import views

app_name = 'user'

urlpatterns = [
    path('<storename>/login/', views.userLogin, name='login'),
    path('<storename>/register/', views.userRegister, name='register'),
    path('<storename>/', views.home, name='home'),
    path('<storename>/shop/', views.shop, name='shop'),
    path('<storename>/about/', views.about, name='about'),
    path('<storename>/contact/', views.contact, name='contact'),
    path('<storename>/shop/<int:id>/',
         views.product_details, name='product-details'),
    path('<storename>/wishlist/', views.wishlist, name='wishlist'),
    path('<storename>/cart/', views.wishlist, name='cart'),
    path('<storename>/checkout/', views.checkout, name='checkout'),


]
