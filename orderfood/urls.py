from django.urls import path
from .views import *

urlpatterns = [
    path('get_all_foods/', GetAllfoods.as_view(), name='GetAllfoods'),
    path('get_food/<int:id>', GetfoodByID.as_view(), name='GetfoodByID'),
    path('add_fvrt_food/', AddOrRemoveFavoriteFood.as_view(), name='AddOrRemoveFavoriteProduct'),
    path('fvrt_foods/', GetAllFavouriteFoods.as_view(), name='GetAllFavouriteFoods'),

    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('cart/remove/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]