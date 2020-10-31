import re
from rest_framework import serializers
from client.models import ClientProfile


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
