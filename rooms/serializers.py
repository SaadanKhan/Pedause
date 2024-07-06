from .models import Room, UserFavouriteRoom, Review, RoomImage, UserRoom
from rest_framework import serializers
from accounts.serializers import CustomUserSerializer


class RoomImageSerializer(CustomUserSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    gallery = RoomImageSerializer(many=True)
    class Meta:
        model = Room
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class UserFvrtRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavouriteRoom
        fields = '__all__'

class UserRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = UserRoom
        fields = '__all__'