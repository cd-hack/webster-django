from django.urls import path,include
from client import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


app_name='client'

router =DefaultRouter()
router.register('user',views.ProfileViewSet)
router.register('website',views.WebsiteViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('login/',obtain_auth_token),
    path('productlist/',views.ProductView.as_view()),
    path('websitelist/',views.WebsiteList.as_view()),
    path('category/<int:pk>/',views.categoryview,name='categoryview'),
    path('fetchproducts/<int:pk>/', views.fetchProducts, name='fetchproducts'),
    path('dashboard/<int:pk>/', views.dashBoard, name='dashboard'),
    path('productdetail/<int:pk>/',views.ProductDetail.as_view()),
    # path('testview/',views.testview,name='testview')
]
