from django.urls import path,include
from client import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


app_name='client'

router =DefaultRouter()
router.register('user',views.ClientViewSet)
router.register('website',views.WebsiteViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('login/',obtain_auth_token),
    path('products/',views.ProductView.as_view())
]
