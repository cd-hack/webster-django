from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from client.serializers import ClientSerializer,WebsiteSerializer,ProductSerializer
from client import models
from client.permissions import ClientPermission,WebsitePermission
from client.paginations import ProductPagination
from rest_framework.generics import ListAPIView
import django_filters.rest_framework


class ClientViewSet(viewsets.ModelViewSet):
    queryset = models.ClientProfile.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ClientPermission,)

class WebsiteViewSet(viewsets.ModelViewSet):
    queryset=models.Website.objects.all()
    serializer_class=WebsiteSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(WebsitePermission,IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class ProductView(ListAPIView):
    pagination_class=ProductPagination
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filterset_fields=[]
    
    def get_queryset(self):
        wwebsite=models.Website.objects.get(pk=self.request.DATA['wid'])
        return wwebsite.product_set.all()
