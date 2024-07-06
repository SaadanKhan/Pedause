from .models import UserRestaurantBooking, Restaurant
from django.utils import timezone

def check_restaurant_availability(rest_id, member):
    try:
        # Get the restaurant instance
        rest = Restaurant.objects.filter(id=rest_id).first()
        rest_capacity = rest.capacity
        
        # Calculate the total number of booked seats for the active bookings
        bookings = UserRestaurantBooking.objects.filter(restaurant_id=rest_id, restaurant__is_active=True)
        booked_by_member = sum(booking.member for booking in bookings)

        # Calculate remaining seats
        remaining_unbooked = rest_capacity - booked_by_member

        # Check if the requested number of seats can be booked
        if remaining_unbooked >= int(member):
            return True
        else:
            return False

    except Exception as e:
        return str(e)
