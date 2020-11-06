import requests
import json
import datetime
from django.db.models.functions import TruncDay
from django.db.models import Count 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from client.serializers import ClientSerializer, WebsiteSerializer, ProductSerializer
from client import models
import user.models
from client.permissions import ClientPermission, WebsitePermission
from client.paginations import ProductPagination
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ClientPermission,)


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = models.Website.objects.all()
    serializer_class = WebsiteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (WebsitePermission, IsAuthenticated)

    def perform_create(self, serializer):
        cp = self.request.user.client_profile
        if cp is None:
            raise serializers.ValidationError(
                {"status": "failed", "message": "clients are only permitted to create website"})
        else:
            serializer.save(client=self.request.user.client_profile)


class ProductView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields=[]

    def get_queryset(self):
        wwebsite = models.Website.objects.get(pk=self.request.data['wid'])
        return wwebsite.product_set.all()


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def fetchProducts(request,pk=None):
    if not pk:
        return Response({"status":"failed","message":"website id argument was not passed"})
    websiteId = pk
    website = models.Website.objects.get(pk=websiteId)
    categories = website.category_set
    if website is None:
        return Response({"status": "failed", "message": "Invalid website ID"}, status=status.HTTP_404_NOT_FOUND)
    elif request.user != website.client.profile:
        return Response({"status": "failed", "message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    else:
        products = []
        url = 'https://www.instagram.com/{}/?__a=1'.format(website.ighandle)
        html = requests.get(url)
        response = json.loads(html.text)
        id = response['graphql']['user']['id']
        has_next_page = True
        end_cursor = ''
        video_count = 0
        while(has_next_page):
            url2 = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&id=' + \
                id+'&first=1000'+end_cursor
            html = requests.get(url2)
            response = json.loads(html.text)
            for i in response['data']['user']['edge_owner_to_timeline_media']['edges']:
                if not i['node']['is_video']:
                    a = dict()
                    a['id'] = i['node']['id']
                    a['url'] = i['node']['display_url']
                    try:
                        a['description'] = i['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    except IndexError:
                        continue
                    a['timestamp'] = i['node']['taken_at_timestamp']
                    products.append(a)
                else:
                    video_count += 1
            has_next_page = response['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            ec = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            if ec is not None:
                end_cursor = '&after='+ec
        for i in products:
            try:
                fp=None
                fd=None
                prodDetails = json.loads(i['description'])
                if not all(x in prodDetails for x in ['name', 'price', 'description', 'productType', 'available', 'category']):
                    continue
                if prodDetails['productType'] == 1:
                    if 'size' not in prodDetails:
                        continue
                    fp=models.FashionProduct.objects.create(size=prodDetails['size'])
                if prodDetails['productType'] == 2:
                    if not all(x in prodDetails for x in ['veg', 'foodType']):
                        continue
                    fd=models.FoodProduct.objects.create(veg=prodDetails['veg'],foodType=prodDetails['foodType'])
                category = categories.get(name=prodDetails['category'])
                if category is None:
                    continue
                obj, created = models.Product.objects.update_or_create(instagramid=i['id'], website=website, date=datetime.datetime.fromtimestamp(int(i['timestamp'])),
                defaults={'name': prodDetails['name'], 'price': float(prodDetails['price']),
                 'description': prodDetails['description'], 'productType': int(prodDetails['productType']),
                 'image': i['url'], 'available': prodDetails['available'], 'category': category,'fashion':fp,'food':fd})
            except:
                continue
        return Response({'status': 'success', 'message': 'Products successfully fetched'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def dashBoard(request,pk=None):
    if not pk:
        return Response({"status":"failed","message":"website id argument was not passed"})
    websiteId = pk
    website = models.Website.objects.get(pk=websiteId)
    if request.user != website.client.profile:
        return Response({"status": "failed", "message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    dash= dict()
    dash['ordergraph']=list(website.order_set.filter(date__gt=datetime.date.today-7).annotate(date=TruncDay('date')).values("date").annotate(created_count=Count('id')).order_by("-date"))
    orders=website.order_set.all()
    dash['order_total']=0
    for i in orders:
        for j in i.orderproduct_set.all():
            dash['order_total']+=j.total
    dash['ordertoday']=website.order_set.filter(date=datetime.date.today).count
    dash['totalorders']=website.order_set.all().count
    dash['status']='success'
    return Response(data=dash,status=status.HTTP_200_OK)