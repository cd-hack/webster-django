import re
import requests
import json
from rest_framework import serializers
from client.models import ClientProfile, Website, Product,FashionProduct,FoodProduct


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('id', 'phone', 'email', 'name',
                  'accNo', 'ifsc', 'plan', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, attrs):
        if not 9 <= len(attrs['accNo']) <= 18:
            raise serializers.ValidationError(
                "Account number should have digits between 9 and 16")
        if len(attrs['phone']) != 10:
            raise serializers.ValidationError(
                "Phone Number should be of length 10")
        if re.match(r'^[a-zA-Z ]+$', attrs['name']) is None:
            raise serializers.ValidationError("Invalid Name")
        if not 1 <= attrs['plan'] <= 2:
            raise serializers.ValidationError("Invalid plan")
        if len(attrs['ifsc']) != 11:
            raise serializers.ValidationError("IFSC Code must be 11 digits")
        return super().validate(attrs)

    def create(self, validated_data):
        client = ClientProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'], accNo=validated_data['accNo'], ifsc=validated_data['ifsc'], plan=validated_data['plan'],
            password=validated_data['password']
        )
        return client


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
        extra_kwargs = {
            'client': {
                'read_only': True,
            }
        }

    def igexists(self, ighandle):
        url = 'https://www.instagram.com/{}/?__a=1'.format(ighandle)
        response = requests.get(url)
        userDetails = json.loads(response.text)
        if 'graphql' not in userDetails:
            return {'status': True, 'message': 'The given Instagram Profile does not exist !!'}
        else:
            return {'status': userDetails['graphql']['user']['is_private'], 'message': 'The given Instagram Profile is Private !!'}

    def validate(self, attrs):
        if not 1 <= attrs['templatetype'] <= 2:
            raise serializers.ValidationError("Invalid template type")
        igstatus = self.igexists(attrs['ighandle'])
        if igstatus['status']:
            raise serializers.ValidationError(igstatus['message'])
        return super().validate(attrs)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(ProductSerializer, self).to_representation(instance)
        is_list_view = isinstance(self.instance, list)
        if is_list_view:
            if ret['productType']==1:
                fash=FashionProduct.objects.get(pk=ret['fashion'])
                extra_ret = {"size":fash.size}
            else:
                food=FoodProduct.objects.get(pk=ret['food'])
                extra_ret={"veg":food.veg,"foodType":food.foodType}
            ret.pop('fashion',None)
            ret.pop('food',None)
            ret.update(extra_ret)
        return ret
