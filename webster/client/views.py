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


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = models.ClientProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ClientPermission,)

class WebsiteViewSet(viewsets.ModelViewSet):
    serializer_class=WebsiteSerializer
    queryset=models.Website.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(WebsitePermission,IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset=models.Product.objects.all()
    authentication_classes=(TokenAuthentication,)
