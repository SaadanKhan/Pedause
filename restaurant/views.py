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


class GetAllRestaurant(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            restaurants = Restaurant.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 10
            rooms_paginated = paginator.paginate_queryset(restaurants, request)
            serializer = RestaurantSerializer(rooms_paginated, many=True)

            paginated_response = paginator.get_paginated_response(serializer.data)

            # Customize the response structure
            return Response({
                'success': True,
                'message': 'All restaurants',
                'data': {
                    'restaurants': paginated_response.data,
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


class GetRestaurantByID(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            restaurant = Restaurant.objects.filter(id=id).first()
            if restaurant:
                serializer = RestaurantSerializer(restaurant)
                return Response({
                    'success': True,
                    'message': 'restaurant',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'success': False,
                    'message': 'restaurant not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class GetRestaurantByCategory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            restaurant = RestaurantCategory.objects.filter(id=id).first()
            if restaurant:
                serializer = RestaurantCategorySerializer(restaurant)
                return Response({
                    'success': True,
                    'message': 'restaurant',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'success': False,
                    'message': 'restaurant not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class FilterRestaurantByName(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            search_query = request.data.get('name', None)
            if search_query:
                restaurant = Restaurant.objects.filter(name__icontains=search_query)
            else:
                restaurant = Restaurant.objects.all()
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            rooms_paginated = paginator.paginate_queryset(restaurant, request)
            serializer = RestaurantSerializer(rooms_paginated, many=True)

            paginated_response = paginator.get_paginated_response(serializer.data)

            # Customize the response structure
            return Response({
                'success': True,
                'message': 'restaurants found' if restaurant.exists() else 'No rooms found',
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
            }, status=status.HTTP_200_OK if restaurant.exists() else status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class AddOrRemoveFavoriteRestaurant(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            restaurant_id = request.data.get('restaurant_id', None)
            if restaurant_id:
                restaurant = Restaurant.objects.filter(id = restaurant_id).first()
                if restaurant:
                    user_fvrt_restaurant = UserFavouriteRestaurant.objects.filter(user = request.user, restaurant = restaurant).first()
                    if user_fvrt_restaurant:
                        user_fvrt_restaurant.delete()
                        return Response({
                            'success': True,
                           'message': 'Restaurant removed from favorites'
                        }, status=status.HTTP_200_OK)
                    else:
                        user_fvrt_restaurant = UserFavouriteRestaurant.objects.create(user = request.user, restaurant = restaurant)
                        return Response({
                            'success': True,
                           'message': 'Restaurant added to favorites'
                        }, status=status.HTTP_201_CREATED)
                    
                else:
                    return Response({
                        'success': False,
                        'message': 'Restaurant not found'
                    }, status=status.HTTP_404_NOT_FOUND)  
                  
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class GetAllFavouriteRestaurant(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_fvrt_restaurant = UserFavouriteRestaurant.objects.filter(user=request.user).all()
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_rooms = paginator.paginate_queryset(user_fvrt_restaurant, request)
            serializer = UserFvrtRestaurantSerializer(paginated_rooms, many=True)
            
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'message': 'Favourite restaurant',
                'data': {
                    'restaurant': paginated_response.data,
                    'pagination': {
                        'count': paginator.page.paginator.count,
                        'page_size': paginator.page_size,
                        'current_page': paginator.page.number,
                        'total_pages': paginator.page.paginator.num_pages,
                        'next': paginated_response.data['next'],
                        'previous': paginated_response.data['previous']
                    }
                }
            }, status=status.HTTP_200_OK if user_fvrt_restaurant.exists() else status.HTTP_404_NOT_FOUND)
            
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
            reviews = RestaurantReview.objects.all()
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_reviews = paginator.paginate_queryset(reviews, request)
            serializer = RestaurantReviewSerializer(paginated_reviews, many=True)
            
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


class BookRestaurant(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get user and room data from request
            user = request.user
            rest_id = request.data.get('rest_id')
            checkin_date = datetime.strptime(request.data.get('checkin_date'), '%Y-%m-%d %H:%M:%S')
            checkout_date = datetime.strptime(request.data.get('checkout_date'), '%Y-%m-%d %H:%M:%S')
            checkin_time = datetime.strptime(request.data.get('checkin_time'), '%H:%M:%S').time()
            member = request.data.get('member')
            full_name = request.data.get('full_name')
            phone = request.data.get('phone')
            govt_id = request.data.get('type_id')
            email = request.data.get('email')
            
            if UserRestaurantBooking.objects.filter(user=request.user, 
                                                    restaurant=rest_id,
                                                    checkin_date=checkin_date,
                                                    checkout_date=checkout_date,
                                                    checkin_time=checkin_time,
                                                    is_active=True
                                                    ).first():
                return Response({
                'success': False,
                'message': 'You have already booked this restaurant'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if room booked
            if check_restaurant_availability(rest_id, member, user) == False:
                return Response({
                'success': False,
                'message': 'Not enough seats available'
                }, status=status.HTTP_400_BAD_REQUEST)
               
            else:
                restaurant = Restaurant.objects.filter(id=rest_id).first()
                if restaurant:
                    custom_user = CustomUser.objects.filter(phone=user).first()
                    custom_user.email = email
                    custom_user.phone = phone
                    custom_user.username = full_name
                    custom_user.govt_id = govt_id
                    custom_user.save()

                    # Book the room for the user
                    user_rest = UserRestaurantBooking.objects.create(
                        user=custom_user, 
                        restaurant=restaurant, 
                        checkin_date=checkin_date, 
                        checkout_date=checkout_date, 
                        checkin_time=checkin_time,
                        member=member)

                    return Response({
                    'success': True,
                    'message': 'Restaurant booked successfully',
                    'data':{
                        'user_name': custom_user.username,
                        'user_number': custom_user.phone,
                        'user_email': custom_user.email,
                        'user_restaurant': user_rest.restaurant.name,
                        'guests': user_rest.member,
                        'checkin_date': user_rest.checkin_date,
                        'checkout_date':user_rest.checkout_date,
                        'checkin_time': user_rest.checkin_time}
                    }, status=status.HTTP_201_CREATED)
                
                else:
                    return Response({
                        'success': False,
                        'message': 'restaurant does not exist'
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class CancelRestaurantBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Get user and room data from request
            user = request.user
            room = Restaurant.objects.filter(id=id).first()
            custom_user = CustomUser.objects.filter(phone=user).first()
            rest_booking = UserRestaurantBooking.objects.filter(room=room, user=user).first()

            if not rest_booking:
                return Response({
                    'success': False,
                    'message': 'No active booking found for this room'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Perform checkout
            rest_booking.is_active = False
            rest_booking.save()

            return Response({
                'success': True,
                'message': 'Checked out successfull',
                'data': {
                    'user_name': custom_user.username,
                    'user_email': custom_user.email,
                    'room_name': rest_booking.restaurant.name,
                    'checkout_date': rest_booking.checkout_date,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
