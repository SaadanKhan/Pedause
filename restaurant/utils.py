from .models import UserRestaurantBooking, Restaurant
from django.utils import timezone


def check_restaurant_availability(rest_id, member, user):
    try:
        rest_bookings = UserRestaurantBooking.objects.filter(user=user, is_active=True)
        for booking in rest_bookings:
            if booking.checkout_date <= timezone.now():
                booking.is_active = False
                booking.save()

        # Get the restaurant instance
        rest = Restaurant.objects.filter(id=rest_id).first()
        rest_capacity = rest.capacity
        
        # Calculate the total number of booked seats
        bookings = UserRestaurantBooking.objects.filter(restaurant_id=rest_id, is_active=True).first()
        if bookings:
            booked_by_member = sum(booking.member for booking in bookings)
            remaining_unbooked = rest_capacity - booked_by_member

            if remaining_unbooked >= int(member):
                return True
            else:
                return False

    except Exception as e:
        return str(e)
