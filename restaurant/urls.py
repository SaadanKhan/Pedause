from django.urls import path
from .views import *

urlpatterns = [
    path('get_all_restaurants/', GetAllRestaurant.as_view(), name='GetAllRestaurant'),
    path('get_restaurant/<int:id>', GetRestaurantByID.as_view(), name='GetRestaurantByID'),
    path('filter_restaurant/', FilterRestaurantByName.as_view(), name='FilterRestaurantByName'),
    path('fvrt_restaurant/', AddOrRemoveFavoriteRestaurant.as_view(), name='AddOrRemoveFavoriteRestaurant'),  
    path('get_fvrt_restaurants/', GetAllFavouriteRestaurant.as_view(), name='UserFavouriteRestaurant'), 
    path('get_all_reviews/', GetAllReviews.as_view(), name='UserReview'),
    path('book_restaurant/', BookRestaurant.as_view(), name='BookRestaurant'),
    path('restaurant_category/<int:id>', GetRestaurantByCategory.as_view(), name='GetRestaurantByCategory'),
    path('cancel_booking/<int:id>', CancelRestaurantBooking.as_view(), name='CancelRestaurantBooking'),
]