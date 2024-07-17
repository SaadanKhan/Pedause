from .models import *
from rest_framework import serializers
from accounts.serializers import CustomUserSerializer


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class UserFvrtFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = UserFavouriteFood
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cartitem = CartItemSerializer(many=True)	
    class Meta:
        model = Cart
        fields = '__all__'