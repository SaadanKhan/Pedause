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
from django.shortcuts import get_object_or_404



class GetAllfoods(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve all rooms
            foods = Food.objects.all()
            
            # Retrieve favorite rooms for the authenticated user
            user_favorite_foods = UserFavouriteFood.objects.filter(user=request.user).values_list('food_id', flat=True)

            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10
            foods_paginated = paginator.paginate_queryset(foods, request)

            # Serialize rooms with an additional 'is_fvrt' field
            foods_data = []
            for food in foods_paginated:
                food_data = FoodSerializer(food).data
                food_data['is_fvrt'] = food.id in user_favorite_foods
                foods_data.append(food_data)

            paginated_response = paginator.get_paginated_response(foods_data)

            # Customize the response structure
            return Response({
                'success': True,
                'message': 'All foods',
                'data': {
                    'foods': paginated_response.data,
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


class GetfoodByID(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            food = Food.objects.filter(id = id).first()
            if food:
                serializer = FoodSerializer(food)
                return Response({
                'success': True,
                'message': 'Food',
                    'data': {
                        serializer.data
                    }
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                   'success': False,
                   'message': 'food not found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class AddOrRemoveFavoriteFood(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            food_id = request.data.get('food_id', None)
            if food_id:
                food = Food.objects.filter(id = food_id).first()
                if food:
                    user_fvrt_food = UserFavouriteFood.objects.filter(user = request.user, food = food).first()
                    if user_fvrt_food:
                        user_fvrt_food.delete()
                        return Response({
                            'success': True,
                           'message': 'Food removed from favorites'
                        }, status=status.HTTP_200_OK)
                    else:
                        user_fvrt_food = UserFavouriteFood.objects.create(user = request.user, food = food)
                        serializer = UserFavouriteFood(user_fvrt_food)
                        return Response({
                            'success': True,
                           'message': 'food added to favorites',
                           'data': serializer.data
                        }, status=status.HTTP_201_CREATED)
                    
                else:
                    return Response({
                        'success': False,
                        'message': 'food not found'
                    }, status=status.HTTP_404_NOT_FOUND)  
                  
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class GetAllFavouriteFoods(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_fvrt_food = UserFavouriteFood.objects.filter(user=request.user).all()
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_foods = paginator.paginate_queryset(user_fvrt_food, request)
            serializer = UserFvrtFoodSerializer(paginated_foods, many=True)
            
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'message': 'Favourite food items',
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
            }, status=status.HTTP_200_OK if user_fvrt_food.exists() else status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class AddToCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        id = request.data.get('food_id')     
        quantity = int(request.data.get('quantity'))

        food_item = Food.objects.filter(id=id).first()
        if not food_item:
            return Response({
                'success': False,
                'message': 'Food item not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        my_items = []
        for _ in range(quantity):
            obj = CartItem.objects.create(user=user, food=food_item)
            my_items.append(obj)

        cart, created = Cart.objects.get_or_create(user=user)

        if not created:
            for item in my_items:
                cart.total_price += item.food.price
                cart.cartitem.add(item)
            cart.save()

        return Response({
            'success': True,
            'message': 'Item added to cart',
            'data': CartSerializer(cart).data
        }, status=status.HTTP_200_OK)


class ViewCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        serializer = CartSerializer(cart)
        return Response({
            'success': True,
            'message': 'Cart retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=user)
        cart.cartitem.remove(cart_item)
        cart.save()
        
        return Response({
            'success': True,
            'message': 'Item removed from cart'
        }, status=status.HTTP_200_OK)