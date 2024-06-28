from django.urls import path
from .views import GetAllRooms, GetRoomsByID, GetUserFavouriteRoom, GetAllReviews, BookRoom, FilterRoomsByName,AddOrRemoveFavoriteRoom, GetAllfavouriteRooms

urlpatterns = [
    path('get_all_rooms/', GetAllRooms.as_view(), name='GetAllRooms'),
    path('get_fvrt_rooms/', GetUserFavouriteRoom.as_view(), name='UserFvrtRooms'),
    path('get_room/<int:id>', GetRoomsByID.as_view(), name='GetRoomByID'),
    path('get_reviews/', GetAllReviews.as_view(), name='GetReviews'),
    path('book_room/', BookRoom.as_view(), name='BookRoom'),
    path('filter_room/', FilterRoomsByName.as_view(), name='FilterRoomsByName'),
    path('add_fvrt_room/', AddOrRemoveFavoriteRoom.as_view(), name='AddOrRemoveFavoriteRoom'),
    path('fvrt_room/', GetAllfavouriteRooms.as_view(), name='GetAllfavouriteRooms'),
]