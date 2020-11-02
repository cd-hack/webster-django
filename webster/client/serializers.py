import re
import requests
import json
from rest_framework import serializers
from client.models import ClientProfile,Website,Product


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
            phone=validated_data['phone'], accNo=validated_data['accNo'], ifsc=validated_data['ifsc'], pan=validated_data['plan'],
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
    def igexists(self,ighandle):
        url='https://www.instagram.com/{}/?__a=1'.format(ighandle)
        response=requests.get(url)
        userDetails=json.loads(response.text)
        if not userDetails.has_key('graphql'):
            return {'status':False,'message':'The given Instagram Profile does not exist !!'}
        else:
            return {'status':userDetails['graphql']['user']['is_private'],'message':'The given Instagram Profile is Private !!'}

    def validate(self, attrs):
        if not 1 <= attrs['templatetype'] <= 2:
            raise serializers.ValidationError("Invalid template type")
        igstatus=self.igexists(attrs['ighandle'])
        if not igstatus['status']:
            raise serializers.ValidationError(igstatus['message'])
        return super().validate(attrs)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def save(self, **kwargs):
        return super().save(**kwargs)
