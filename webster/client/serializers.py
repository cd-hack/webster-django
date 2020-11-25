import re
import requests
from rest_framework import serializers
from client.models import Profile, Website, Product,FashionProduct,FoodProduct,Category
# from user.models import Wishlist,OrderProduct,Rating
from django.db import IntegrityError


class ClientSerializer(serializers.ModelSerializer):
    accNo=serializers.SerializerMethodField()
    plan=serializers.SerializerMethodField()
    ifsc=serializers.SerializerMethodField()
    website=serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ("id","phone","name","email","is_client","is_user","accNo","plan","ifsc","website","user_profile","client_profile")
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
    
    def get_accNo(self,obj):
        print(obj)
        return obj.client_profile.accNo if obj.client_profile is not None else None
    def get_plan(self,obj):
        return obj.client_profile.plan if obj.client_profile is not None else None
    def get_ifsc(self,obj):
        return obj.client_profile.ifsc if obj.client_profile is not None else None
    def get_website(self,obj):
        return obj.user_profile.website if obj.user_profile is not None else None

    def to_internal_value(self, attrs):
        for x in ["phone","name","email","is_client","is_user","password"]:
            if x not in attrs.keys():
                raise serializers.ValidationError({"status":"failed","message":"{} attribute not defined".format(x)})
        if attrs['is_user']==attrs['is_client']:
            raise serializers.ValidationError({"status":"failed","message":"Select either Client or User"})
        if attrs['is_client']:
            for x in ['accNo','plan','ifsc']:         
                if x not in attrs.keys(): 
                    raise serializers.ValidationError({"status":"failed","message":"{} attribute not received".format(x)})
            if not 9 <= len(attrs['accNo']) <= 18:
                raise serializers.ValidationError(
                   {"status":"failed","message": "Account number should have digits between 9 and 16"})
            if not 1 <= attrs['plan'] <= 2:
                raise serializers.ValidationError({"status":"failed","message":"Invalid plan"})
            if len(attrs['ifsc']) != 11:
                raise serializers.ValidationError({"status":"failed","message":"IFSC Code must be 11 digits"})
        if len(attrs['phone']) != 10:
            raise serializers.ValidationError(
                {"status":"failed","message":"Phone Number should be of length 10"})
        if re.match(r'^[a-zA-Z ]+$', attrs['name']) is None:
            raise serializers.ValidationError({"status":"failed","message":"Invalid Name"})
        return attrs

    def to_representation(self, instance):
        print('hello')
        ret = super(ClientSerializer, self).to_representation(instance)
        isview = isinstance(self.instance, object)
        if isview:
            print('hi')
            w=Profile.objects.get(pk=ret['id']).client_profile.website_set.all()
            extra_ret={'websites_owned':[i.id for i in w]}
            ret.update(extra_ret)
        print(isview)
        return ret


    def create(self, validated_data):
        print('hi')
        print(validated_data)
        try:
            if validated_data['is_client']:
                client = Profile.objects.create_user(
                    email=validated_data['email'],
                    name=validated_data['name'],
                    phone=validated_data['phone'], accNo=validated_data['accNo'], ifsc=validated_data['ifsc'], plan=validated_data['plan'],
                    password=validated_data['password'],is_user=validated_data['is_user'],is_client=validated_data['is_client']
                )
                return client
            elif validated_data['is_user']:
                client = Profile.objects.create_user(
                    email=validated_data['email'],
                    name=validated_data['name'],
                    phone=validated_data['phone'],
                    password=validated_data['password'],is_user=validated_data['is_user'],is_client=validated_data['is_client'],website=validated_data.get('website',None)
                )
                return client
        except IntegrityError:
            raise serializers.ValidationError({"status":"failed","message":"Account with same email or phone number exists"})


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
        extra_kwargs = {
            'client': {
                'read_only': True,
            }
        }

    # def igexists(self, ighandle):
    #     url = 'https://www.instagram.com/{}/?__a=1'.format(ighandle)
    #     userDetails = requests.get(url).json()
    #     if 'graphql' not in userDetails:
    #         return {'status': True, 'message': 'The given Instagram Profile does not exist !!'}
    #     else:
    #         return {'status': userDetails['graphql']['user']['is_private'], 'message': 'The given Instagram Profile is Private !!'}

    def validate(self, attrs):
        if not 1 <= attrs['templatetype'] <= 2:
            raise serializers.ValidationError("Invalid template type")
        # if len(attrs['iguserid'])!=10:
        #     raise serializers.ValidationError("Invalid Instagram User ID")
        # igstatus = self.igexists(attrs['ighandle'])
        # if igstatus['status']:
        #     raise serializers.ValidationError({"status":"failed","message":igstatus['message']})
        # if attrs['client'] is None:
        #     raise serializers.ValidationError({"status":"failed","message":"clients are only permitted to create website"})
        return super().validate(attrs)

    def to_representation(self, instance):
        ret= super().to_representation(instance)
        is_object_view=isinstance(self.instance,object)
        if is_object_view:
            website=Website.objects.get(pk=ret['id'])
            extra_ret={'category':[]}
            for i in website.category_set.all():
                extra_ret['category'].append(i.name)
            ret.update(extra_ret)
        return ret

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(ProductSerializer, self).to_representation(instance)
        #print(ret)
        is_list_view = isinstance(self.instance, list)
        is_object_view=isinstance(self.instance,object)
        if is_list_view:
            sum=0
            prod=Product.objects.get(pk=ret['id'])
            count=prod.rating_set.all().count()
            for i in prod.rating_set.all():
                sum+=i.rating
            if count!=0: 
                sum=float(sum)/count
            cat=Category.objects.get(pk=ret['category'])
            extra_ret={'category':cat.name,'rating':str(sum)}
            ret.pop('description',None)
            ret.pop('website',None)
            ret.pop('instagramid',None)
            ret.pop('fashion',None)
            ret.pop('food',None)
            ret.update(extra_ret)
        elif is_object_view:
            product=Product.objects.get(pk=ret['id'])
            extra_ret=dict()
            if ret['productType']==1:
                fash=FashionProduct.objects.get(pk=ret['fashion'])
                extra_ret = {"size":fash.size}
            else:
                food=FoodProduct.objects.get(pk=ret['food'])
                extra_ret={"veg":food.veg,"foodType":food.foodType}
            cat=Category.objects.get(pk=ret['category'])
            extra_ret['categoryname']=cat.name
            extra_ret['wishlistno']=product.wishlist_set.all().count()
            extra_ret['reviews']=[]
            for i in product.rating_set.all():
                a=dict()
                a['rating']=i.rating
                a['review']=i.review
                extra_ret['review'].append(a)
            extra_ret['orderno']=product.orderproduct_set.all().count()
            ret.pop('fashion',None)
            ret.pop('food',None)
            ret.pop('category',None)
            ret.update(extra_ret)
        return ret
