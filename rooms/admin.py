from django.contrib import admin
from .models import Room, Review, RoomImage, UserRoom, UserFavouriteRoom


@admin.register(UserRoom)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']

@admin.register(Review)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']

@admin.register(UserFavouriteRoom)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']


admin.site.register(Room)
admin.site.register(RoomImage)
