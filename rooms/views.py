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
from accounts.models import CustomUser
from datetime import datetime
from django.utils import timezone


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
                'data': {
                    serializer.data 
                }
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
                    'data': {
                        serializer.data
                    }
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


class FilterRoomsByName(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            search_query = request.data.get('name', None)
            if search_query:
                rooms = Room.objects.filter(name__icontains=search_query)
            else:
                rooms = Room.objects.all()
            
            if rooms.exists():
                serializer = RoomSerializer(rooms, many=True)
                return Response({
                    'success': True,
                    'message': 'Rooms found',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'No rooms found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class AddOrRemoveFavoriteRoom(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            room_id = request.data.get('room_id', None)
            if room_id:
                room = Room.objects.filter(id = room_id).first()
                if room:
                    user_fvrt_room = UserFavouriteRoom.objects.filter(user = request.user, room = room).first()
                    if user_fvrt_room:
                        user_fvrt_room.delete()
                        return Response({
                            'success': True,
                           'message': 'Room removed from favorites'
                        }, status=status.HTTP_200_OK)
                    else:
                        user_fvrt_room = UserFavouriteRoom.objects.create(user = request.user, room = room)
                        return Response({
                            'success': True,
                           'message': 'Room added to favorites'
                        }, status=status.HTTP_201_CREATED)
                    
                else:
                    return Response({
                        'success': False,
                        'message': 'Room not found'
                    }, status=status.HTTP_404_NOT_FOUND)  
                  
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        

class GetAllfavouriteRooms(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_fvrt_room = UserFavouriteRoom.objects.filter(user = request.user).all()
            if user_fvrt_room:
                serializer = UserFvrtRoomSerializer(user_fvrt_room, many=True)
                return Response({
                    'success': True,
                   'message': 'Favourite rooms',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'success': False,
                   'message': 'No room found'
                }, status=status.HTTP_404_NOT_FOUND)
                  
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
                    'data': {
                        serializer.data
                    }
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


class GetAllReviews(APIView):
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
                    'data': {
                        serializer.data
                    }
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
        

class BookRoom(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get user and room data from request
            user = request.user
            room_id = request.data.get('room_id')
            checkin_date = datetime.strptime(request.data.get('checkin_date'), '%Y-%m-%d %H:%M:%S')
            checkout_date = datetime.strptime(request.data.get('checkout_date'), '%Y-%m-%d %H:%M:%S')

            # Check if room exists
            room_bookings = UserRoom.objects.all()
            if room_bookings:
                for room in room_bookings:
                    if room.checkout_date >= timezone.now():
                        room.delete()
            
            booked_room = UserRoom.objects.filter(room=room_id).first()
            if booked_room:
                return Response({
                'success': False,
                'message': 'Room already booked'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                member = request.data.get('members')
                room = Room.objects.filter(id=room_id).first()
                if room:
                    if int(member) > room.members:
                        return Response({
                        'success': False,
                        'message': 'Room capacity exceeded'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    full_name = request.data.get('full_name')
                    phone = request.data.get('phone')
                    govt_id = request.data.get('type_id')
                    email = request.data.get('email')
                    account_balance = float(request.data.get('account_balance'))

                    # Calculate either a user can afford to pay
                    duration = checkin_date - checkout_date
                    days_to_stay = duration.days
                    total_expense = room.price_per_day * days_to_stay

                    if account_balance < total_expense:
                        return Response({
                        'success': False,
                        'message': 'Insufficient account balance'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    else:
                        custom_user = CustomUser.objects.filter(phone=user).first()
                        custom_user.email = email
                        custom_user.phone = phone
                        custom_user.username = full_name
                        custom_user.govt_id = govt_id
                        custom_user.account_balance = account_balance

                        # Deduct the account balance
                        custom_user.account_balance = account_balance - total_expense

                        # Book the room for the user
                        UserRoom.objects.create(user=user, room=room, checkin_date=checkin_date,
                                                        checkout_date=checkout_date)

                        return Response({
                        'success': True,
                        'message': 'Room booked successfully'
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                else:
                    return Response({
                        'success': False,
                        'message': 'Room does not exist'
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
