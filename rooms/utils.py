from accounts.models import CustomUser
from .models import Room, UserRoom
from django.utils import timezone


def check_room_availability(room_id, checkin_date):
    try:
        room_bookings = UserRoom.objects.filter(room=room_id, 
                                                is_active=True, 
                                                checkin_date=checkin_date
                                                ).first()
        if room_bookings:
            if room_bookings.checkout_date <= timezone.now():
                room_bookings.is_active = False
                room_bookings.save()
                return False
            
            return True
        
        return False
    
    except Exception as e:
        return str(e)