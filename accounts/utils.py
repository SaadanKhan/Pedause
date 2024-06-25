from django.utils import timezone
from twilio.rest import Client
import random
from .models import CustomUser

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