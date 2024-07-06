from django.urls import path
from .views import *

urlpatterns = [
    path('get_all_rooms/', GetAllRooms.as_view(), name='GetAllRooms'),
    path('get_fvrt_rooms/', GetUserFavouriteRoom.as_view(), name='UserFvrtRooms'),
    path('get_room/<int:id>', GetRoomsByID.as_view(), name='GetRoomByID'),
    path('get_reviews/', GetAllReviews.as_view(), name='GetReviews'),
    path('book_room/', BookRoom.as_view(), name='BookRoom'),
    path('filter_room/', FilterRoomsByName.as_view(), name='FilterRoomsByName'),
    path('add_fvrt_room/', AddOrRemoveFavoriteRoom.as_view(), name='AddOrRemoveFavoriteRoom'),
    path('fvrt_room/', GetAllFavouriteRooms.as_view(), name='GetAllfavouriteRooms'),
    path('room_ticket/<int:id>', ViewTicket.as_view(), name='ViewTicket'),
    path('all_bookings/', AllBookings.as_view(), name='AllBookings'),
    path('cancel_booking/<int:id>', CancelBooking.as_view(), name='CancelBooking'),
    path('ongoing_bookings/', OngoingBookings.as_view(), name='OngoingBookings'),
    path('complete_bookings/', CompletedBookings.as_view(), name='CompletedBookings'),
    path('leave_review/<int:id>', LeaveReview.as_view(), name='LeaveReview'),    
]