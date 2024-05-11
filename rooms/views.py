from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class GetAllRooms(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            rooms = Room.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 10
            rooms_paginated = paginator.paginate_queryset(rooms, request)
            serializer = RoomSerializer(rooms_paginated, many=True)

            return paginator.get_paginated_response({
                'success': True,
                'message': 'All rooms',
                'data': serializer.data 
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class GetRoomsByID(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            room = Room.objects.filter(id = id).first()
            if room:
                serializer = RoomSerializer(room)
                return Response({
                'success': True,
                'message': 'Room',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                   'success': False,
                   'message': 'room not found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class GetUserFavouriteRoom(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user_fvrt_room = UserFavouriteRoom.objects.filter(user = request.user).first()
            if user_fvrt_room:
                serializer = UserFvrtRoomSerializer(user_fvrt_room)

                return Response({
                'success': True,
                'message': 'Room',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                   'success': False,
                   'message': 'room not found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class GetReviews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            reviews = Review.objects.all()
            if reviews:
                serializer = ReviewSerializer(reviews, many=True)

                return Response({
                'success': True,
                'message': 'Reviews',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                   'success': False,
                   'message': 'no reviews'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        

