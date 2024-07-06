from django.utils import timezone
from twilio.rest import Client
import random
from .models import CustomUser
from rooms.models import Room, UserRoom

def generate_unique_phone():
    while True:
        phone = str(random.randint(10**10, 10**11 - 1))
        if not CustomUser.objects.filter(phone=phone).exists():
            return phone


def is_valid_otp(user):
    try:
        time_difference = timezone.now() - user.otp_created_at
        if time_difference.total_seconds() <= 120:
            return True
        return False
    except Exception as e:
        print(e)


def check_room_availability(room_id):
    try:
        room_bookings = UserRoom.objects.all()
        if room_bookings:
            for room in room_bookings:
                if room.checkout_date >= timezone.now():
                    room.is_active = False
                    room.save()

        booked_room = UserRoom.objects.filter(room=room_id, is_active=True).first()
        return booked_room
    
    except Exception as e:
        return str(e)


"""
sending a message by using twilio
"""
def send_message(user_otp, user_phone):
    try:
        account_sid = 'AC1632b3415d66ac4a244bf96324997fff'
        auth_token = 'ed355c44bd9ff005d47b587975f7617a'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=user_otp,
            from_='+19096382958',
            to=str(user_phone)
            )
        print(message.sid)

    except Exception as e:
        print(e)