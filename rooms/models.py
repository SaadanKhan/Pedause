from django.db import models
from accounts.models import CustomUser


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    stars = models.IntegerField(null=True, blank=True)
    review_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room.name} Review"


class Room(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    main_image = models.ImageField(upload_to='uploads/', default='static/uploads/room.jpeg')
    category = models.CharField(max_length=100, null=True, blank=True)
    bed = models.IntegerField(null=True, blank=True, default=1)
    bathroom = models.IntegerField(null=True, blank=True, default=1)
    price_per_day = models.IntegerField(null=True, blank=True)
    about = models.TextField(null=True, blank=True, default="About the Room")
    gallery = models.ManyToManyField('RoomImage', related_name='room_gallery', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class RoomImage(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/', default='static/uploads/room.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class UserRoom(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class UserFavouriteRoom(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username