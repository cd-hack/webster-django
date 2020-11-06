from django.urls import path, include
from user import views

app_name = 'user'

urlpatterns = [
    path('<storename>/', views.home, name='home'),
    path('<storename>/shop/', views.shop, name='shop'),

]
