from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from client.serializers import ClientSerializer
from client import models
from client.permissions import ClientPermission


class CLientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = models.ClientProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ClientPermission,)
