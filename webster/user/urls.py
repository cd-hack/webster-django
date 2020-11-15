from django.urls import path, include
from user import views

app_name = 'user'

urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('<storename>/login/', views.userLogin, name='login'),
    path('<storename>/register/', views.userRegister, name='register'),
    path('<storename>/', views.home, name='home'),
    path('<storename>/shop/', views.shop, name='shop'),
    path('<storename>/about/', views.about, name='about'),
    path('<storename>/contact/', views.contact, name='contact'),
    path('<storename>/shop/<int:id>/',
         views.product_details, name='product-details'),
    path('<storename>/wishlist/', views.wishlist, name='wishlist'),
    path('<storename>/cart/', views.cart, name='cart'),
    path('<storename>/checkout/', views.checkout, name='checkout'),
    path('<storename>/shop/<int:id>/add-to-wishlist/',
         views.add_to_wishlist, name='add-to-wishlist'),
    path('<storename>/shop/<int:id>/add-to-cart/',
         views.add_to_cart, name='add-to-cart'),
    path('<storename>/wishlist/<int:id>/remove-from-cart/',
         views.remove_from_cart, name='remove-from-cart'),
    path('<storename>/wishlist/<int:id>/remove-from-wishlist/',
         views.remove_from_wishlist, name='remove-from-wishlist'),
    path('<storename>/logout/',
         views.userLogout, name='logout'),
    path('<storename>/write-review/<int:id>/',
         views.write_review, name='write-review'),




]
