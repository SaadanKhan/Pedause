from . models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .utils import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create(
            phone = validated_data.get('phone'),
            email = validated_data.get('email'),
            password = make_password(validated_data.get('password'))
        )
        return user 


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'
        extra_kwargs = {
            'phone': {'required': False}
        }

    def create(self, validated_data): 
        random_phone = generate_unique_phone()

        social_account = SocialAccount.objects.create(
            user = CustomUser.objects.create(
                phone = random_phone,
                email = validated_data.get('email'),
                is_verified = True),
                
            apple_id = validated_data.get('apple_id', None),
            name = validated_data.get('name'),
            phone= random_phone,
            type = validated_data.get('type'),
            email=validated_data.get('email')
            )
        return social_account