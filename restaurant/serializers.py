from .models import *
from rest_framework import serializers
from accounts.serializers import CustomUserSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = '__all__'


class UserFvrtRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavouriteRestaurant
        fields = '__all__'


class RestaurantReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    room = RestaurantSerializer(read_only=True)
    class Meta:
        model = RestaurantReview
        fields = '__all__'