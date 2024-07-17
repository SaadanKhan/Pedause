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
            # Retrieve all rooms
            rooms = Room.objects.all()
            
            # Retrieve favorite rooms for the authenticated user
            user_favorite_rooms = UserFavouriteRoom.objects.filter(user=request.user).values_list('room_id', flat=True)

            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10
            rooms_paginated = paginator.paginate_queryset(rooms, request)

            # Serialize rooms with an additional 'is_fvrt' field
            rooms_data = []
            for room in rooms_paginated:
                room_data = RoomSerializer(room).data
                room_data['is_fvrt'] = room.id in user_favorite_rooms
                rooms_data.append(room_data)

            paginated_response = paginator.get_paginated_response(rooms_data)

            # Customize the response structure
            return Response({
                'success': True,
                'message': 'All rooms',
                'data': {
                    'rooms': paginated_response.data,
                    'pagination': {
                        'count': paginator.page.paginator.count,
                        'page_size': paginator.page_size,
                        'current_page': paginator.page.number,
                        'total_pages': paginator.page.paginator.num_pages,
                        'next': paginated_response.data['next'],
                        'previous': paginated_response.data['previous']
                    }
                }
            }, status=status.HTTP_200_OK)
            
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
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            rooms_paginated = paginator.paginate_queryset(rooms, request)
            serializer = RoomSerializer(rooms_paginated, many=True)

            paginated_response = paginator.get_paginated_response(serializer.data)

            # Customize the response structure
            return Response({
                'success': True,
                'message': 'Rooms found' if rooms.exists() else 'No rooms found',
                'data': {
                    'rooms': paginated_response.data,
                    'pagination': {
                        'count': paginator.page.paginator.count,
                        'page_size': paginator.page_size,
                        'current_page': paginator.page.number,
                        'total_pages': paginator.page.paginator.num_pages,
                        'next': paginated_response.data['next'],
                        'previous': paginated_response.data['previous']
                    }
                }
            }, status=status.HTTP_200_OK if rooms.exists() else status.HTTP_404_NOT_FOUND)
        
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
                        serializer = UserFvrtRoomSerializer(user_fvrt_room)
                        return Response({
                            'success': True,
                           'message': 'Room added to favorites',
                           'data': serializer.data
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
        

class GetAllFavouriteRooms(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_fvrt_room = UserFavouriteRoom.objects.filter(user=request.user).all()
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_rooms = paginator.paginate_queryset(user_fvrt_room, request)
            serializer = UserFvrtRoomSerializer(paginated_rooms, many=True)
            
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'message': 'Favourite rooms',
                'data': {
                    'rooms': paginated_response.data,
                    'pagination': {
                        'count': paginator.page.paginator.count,
                        'page_size': paginator.page_size,
                        'current_page': paginator.page.number,
                        'total_pages': paginator.page.paginator.num_pages,
                        'next': paginated_response.data['next'],
                        'previous': paginated_response.data['previous']
                    }
                }
            }, status=status.HTTP_200_OK if user_fvrt_room.exists() else status.HTTP_404_NOT_FOUND)
            
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
            user_fvrt_rooms = UserFavouriteRoom.objects.filter(user=request.user)
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_rooms = paginator.paginate_queryset(user_fvrt_rooms, request)
            serializer = UserFvrtRoomSerializer(paginated_rooms, many=True)
            
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'message': 'Favourite rooms',
                'data': {
                    'rooms': paginated_response.data,
                    'pagination': {
                        'count': paginator.page.paginator.count,
                        'page_size': paginator.page_size,
                        'current_page': paginator.page.number,
                        'total_pages': paginator.page.paginator.num_pages,
                        'next': paginated_response.data['next'],
                        'previous': paginated_response.data['previous']
                    }
                }
            }, status=status.HTTP_200_OK)
        
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
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_reviews = paginator.paginate_queryset(reviews, request)
            serializer = ReviewSerializer(paginated_reviews, many=True)
            
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'message': 'Reviews',
                'data': {
                    'reviews': paginated_response.data,
                    'pagination': {
                        'count': paginator.page.paginator.count,
                        'page_size': paginator.page_size,
                        'current_page': paginator.page.number,
                        'total_pages': paginator.page.paginator.num_pages,
                        'next': paginated_response.data['next'],
                        'previous': paginated_response.data['previous']
                    }
                }
            }, status=status.HTTP_200_OK if reviews.exists() else status.HTTP_404_NOT_FOUND)
        
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

            if checkin_date < timezone.datetime.now() or checkout_date < checkin_date:
                return Response({
                'success': False,
                'message': 'Select the correct dates'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if room booked
            if check_room_availability(room_id, checkin_date):
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
                    duration = checkout_date - checkin_date
                    days_to_stay = duration.days
                    total_expense = room.price_per_day * days_to_stay

                    print('days to stay', days_to_stay)
                    print('total expense', total_expense)
                    print('account balance', account_balance)



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
                        custom_user.save()

                        # Book the room for the user
                        user_room = UserRoom(user=custom_user, room=room, checkin_date=checkin_date, checkout_date=checkout_date, total_expense=total_expense)
                        user_room.save()

                        # Create a ticket
                        ticket = RoomTicket(user=custom_user, room=room, checkin_date=checkin_date, checkout_date=checkout_date)
                        ticket.save()

                        return Response({
                        'success': True,
                        'message': 'Room booked successfully',
                        'data':{
                            'user_name': custom_user.username,
                            'user_number': custom_user.phone,
                            'user_email': custom_user.email,
                            'user_room': user_room.room.name,
                            'guests': member,
                            'checkin_date': checkin_date,
                            'checkout_date':checkout_date
                        }
                        }, status=status.HTTP_201_CREATED)
                
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


class CancelBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Get user and room data from request
            user = request.user
            room = Room.objects.filter(id=id).first()
            custom_user = CustomUser.objects.filter(phone=user).first()
            room_booking = UserRoom.objects.filter(room=room, user=user).first()

            if not room_booking:
                return Response({
                    'success': False,
                    'message': 'No active booking found for this room'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Perform checkout
            # room_booking.checkout_date = timezone.now()
            room_booking.is_active = False
            room_booking.save()

            # update user account balance if necessary
            custom_user = CustomUser.objects.filter(id=user.id).first()
            custom_user.account_balance += room_booking.total_expense
            custom_user.save()

            return Response({
                'success': True,
                'message': 'Booking successfully cancelled',
                'data': {
                    'user_name': custom_user.username,
                    'user_email': custom_user.email,
                    'room_name': room_booking.room.name,
                    'account_balance': custom_user.account_balance
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class AllBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get user and room data from request
            user = request.user
            all_room_booking = UserRoom.objects.all()
            room_booking = []
            
            for booking in all_room_booking:
                if booking.user == user:
                    room_booking.append(booking)

            if room_booking:
                serializer = UserRoomSerializer(room_booking, many=True)
                return Response({
                    'success': True,
                    'message': 'All Bookings',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'success': False,
                    'message': 'No active bookings found for you'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class OngoingBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get user and room data from request
            user = request.user
            room_booking = UserRoom.objects.filter(user=user, is_active=True)
            
            if room_booking:
                serializer = UserRoomSerializer(room_booking, many=True)
                return Response({
                    'success': True,
                    'message': 'Ongoing Bookings',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'No active bookings found for you'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CompletedBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get user and room data from request
            user = request.user
            room_booking = UserRoom.objects.filter(user=user, is_active=False)
            
            if room_booking:
                serializer = UserRoomSerializer(room_booking, many=True)
                return Response({
                    'success': True,
                    'message': 'Completed Bookings',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'success': False,
                    'message': 'No active bookings found for you'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)    


class LeaveReview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            # Get user and room data from request
            user = request.user
            stars = request.data.get('stars')
            review_desc = request.data.get('review_desc')
            room = Room.objects.filter(id=id).first()
            
            Review.objects.create(
                user=user, 
                room=room,
                stars=stars,
                review_desc=review_desc)
            
            return Response({
                'success': True,
                'message': 'Review submitted successfully',
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ViewTicket(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Get user and room data from request
            user = request.user
            room = Room.objects.filter(id=id).first()
            room_ticket = RoomTicket.objects.filter(user=user, room=room).first()
            
            if room_ticket:
                return Response({
                    'success': True,
                    'message': 'Room ticket',
                    'data': {
                        'ticket_number': room_ticket.id,
                        'room_name': room.name,
                        'checkin_date': room_ticket.checkin_date,
                        'checkout_date': room_ticket.checkout_date}
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'message': 'No room ticket found for this room'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

