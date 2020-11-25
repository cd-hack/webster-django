import requests
import json
import datetime
import re
from django.db.models.functions import TruncDay
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from client.serializers import ClientSerializer, WebsiteSerializer, ProductSerializer
from client import models
import user.models
from client.permissions import ClientPermission, WebsitePermission
from client.paginations import ProductPagination
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ClientPermission,)
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['email', 'phone', ]

    def partial_update(self, request, pk=None):
        if not (request.user.is_authenticated and request.user.id != pk):
            return Response(data={"status": "failed", "message": "Unknown credentials"}, status=status.HTTP_403_FORBIDDEN)
        password = request.data.get('password', None)
        if password is None:
            return Response(data={"status": "failed", "message": "Enter password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.user)
        if not request.user.check_password(password):
            return Response(data={"status": "failed", "message": "Password entered is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        ifsc = request.data.get('ifsc', None)
        accNo = request.data.get('accNo', None)
        if email is not None:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not re.search(regex, email):
                Response(data={"status": "failed", "message": "Invalid Email"},
                         status=status.HTTP_400_BAD_REQUEST)
            if Profile.objects.filter(email=email).count() == 0:
                request.user.email = email
                request.user.save()
                return Response(data={"status": "success", "message": "Email changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"status": "failed", "message": "Account with this Email address already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if phone is not None:
            if len(phone) != 10:
                return Response(data={"status": "failed", "message": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)
            if Profile.objects.filter(phone=phone).count() == 0:
                request.user.phone = phone
                request.user.save()
                return Response(data={"status": "success", "message": "Phone number changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"status": "failed", "message": "Account with this Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if ifsc is not None and accNo is not None:
            request.user.client_profile.ifsc = ifsc
            request.user.client_profile.accNo = accNo
            request.user.client_profile.save()
            request.user.save()
            return Response(data={"status": "success", "message": "Account details changed successfully"}, status=status.HTTP_200_OK)
        return Response(data={"status": "failed", "message": "Parameters not found"}, status=status.HTTP_400_BAD_REQUEST)


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
        wwebsite = models.Website.objects.get(pk=self.request.GET.get('wid'))
        return wwebsite.product_set.all()


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Product.objects.get(pk=pk)
        except models.Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prod = self.get_object(pk)
        serializer = ProductSerializer(prod)
        return Response(serializer.data)


class WebsiteList(ListAPIView):
    serializer_class = WebsiteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.client_profile is not None:
            return user.client_profile.website_set.all()
        else:
            return models.Website.none()


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def categoryview(request, pk=None):
    if not pk:
        return Response({"status": "failed", "message": "website id argument was not passed"}, status=status.HTTP_400_BAD_REQUEST)
    websiteId = pk
    website = models.Website.objects.get(pk=websiteId)
    if website is None:
        return Response({"status": "failed", "message": "Invalid website ID"}, status=status.HTTP_404_NOT_FOUND)
    elif request.user != website.client.profile:
        return Response({"status": "failed", "message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    else:
        if request.method == 'POST':
            catlist = request.data['category']
            for i in catlist:
                newc = models.Category.objects.create(name=i, website=website)
            return Response({"status": "success", "message": "Categories successfully added"}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            data = dict()
            data['data'] = list(website.category_set.all())
            data['status'] = 'success'
            return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def fetchProducts(request, pk=None):
    if not pk:
        return Response({"status": "failed", "message": "website id argument was not passed"}, status=status.HTTP_400_BAD_REQUEST)
    websiteId = pk
    website = models.Website.objects.get(pk=websiteId)
    categories = website.category_set
    if website is None:
        return Response({"status": "failed", "message": "Invalid website ID"}, status=status.HTTP_404_NOT_FOUND)
    elif request.user != website.client.profile:
        return Response({"status": "failed", "message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    else:
        products = []
        # url = 'https://www.instagram.com/{}/?__a=1'.format(website.ighandle)
        # html = requests.get(url)
        # response = json.loads(html.text)
        id = website.iguserid
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
                    a['url320'] = i['node']['thumbnail_resources'][2]['src']
                    a['url480'] = i['node']['thumbnail_resources'][3]['src']
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
        # print(products)
        for i in products:
            # try:
                print(i['description'])
                fp = None
                fd = None
                prodDetails = json.loads(i['description'])
                if not all(x in prodDetails for x in ['name', 'price', 'description', 'productType', 'available', 'category']):
                    print('bro no')
                    continue
                if prodDetails['productType'] == 1:
                    if 'size' not in prodDetails:
                        continue
                    fp = models.FashionProduct.objects.create(
                        size=prodDetails['size'])
                if prodDetails['productType'] == 2:
                    if not all(x in prodDetails for x in ['veg', 'foodType']):
                        print('hey no')
                        continue
                    fd = models.FoodProduct.objects.create(
                        veg=prodDetails['veg'], foodType=prodDetails['foodType'])
                category = categories.get(name=prodDetails['category'])
                if category is None:
                    print('no')
                    continue
                obj, created = models.Product.objects.update_or_create(instagramid=i['id'], website=website, date=datetime.datetime.fromtimestamp(int(i['timestamp'])),
                                                                       defaults={'name': prodDetails['name'], 'price': float(prodDetails['price']),
                                                                                 'description': prodDetails['description'], 'productType': int(prodDetails['productType']),
                                                                                 'image': i['url'], 'available': prodDetails['available'], 'category': category, 'fashion': fp, 'food': fd, 'image320': i['url320'], 'image480': i['url480']})
                print(created)
            # except:
            #     print('hello brooooooooo')
            #     continue
        return Response({'status': 'success', 'message': 'Products successfully fetched'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def dashBoard(request, pk=None):
    if not pk:
        return Response({"status": "failed", "message": "website id argument was not passed"})
    websiteId = pk
    website = models.Website.objects.get(pk=websiteId)
    if request.user != website.client.profile:
        return Response({"status": "failed", "message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    dash = dict()
    week_ago = datetime.date.today()-datetime.timedelta(days=7)
    dateqset = website.order_set.filter(
        orderDate__gt=week_ago.strftime("%Y-%m-%d"))
    print(dateqset)
    dash['ordergraph'] = []
    today = datetime.date.today()
    for i in range(6, -1, -1):
        dash['ordergraph'].append(dateqset.filter(orderDate=(
            today-datetime.timedelta(days=i)).strftime("%Y-%m-%d")).count())
    print(dash['ordergraph'])
    orders = website.order_set.all()
    dash['order_total'] = 0
    for i in orders:
        for j in i.orderproduct_set.all():
            dash['order_total'] += j.total
    dash['ordertoday'] = website.order_set.filter(
        orderDate=datetime.date.today().strftime("%Y-%m-%d")).count()
    dash['totalorders'] = website.order_set.all().count()
    dash['usertotal'] = website.userprofile_set.all().count()
    dash['status'] = 'success'
    return Response(data=dash, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def testview(request):
#     response = requests.get(
#         'https://www.instagram.com/a.nandhakris/', verify=False)
#     return Response(data={'data': response.text}, status=status.HTTP_200_OK)
