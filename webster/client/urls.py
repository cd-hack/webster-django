from django.urls import path
from client import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


app_name='client'

router =DefaultRouter()


urlpatterns = [
    path('login/',obtain_auth_token),


]
