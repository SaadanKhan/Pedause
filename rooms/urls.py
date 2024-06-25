from django.urls import path
from .views import GetAllRooms, GetRoomsByID, GetUserFavouriteRoom, GetReviews, BookRoom


urlpatterns = [
    path('get_all_rooms/', GetAllRooms.as_view(), name='GetAllRooms'),
    path('get_fvrt_rooms/', GetUserFavouriteRoom.as_view(), name='UserFvrtRooms'),
    path('get_room/<int:id>', GetRoomsByID.as_view(), name='GetRoomByID'),
    path('get_reviews/', GetReviews.as_view(), name='GetReviews'),
    path('book_room/', BookRoom.as_view(), name='BookRoom'),
]