from django.contrib import admin
from .models import *


admin.site.register(RestaurantCategory)
admin.site.register(Restaurant)

@admin.register(UserRestaurantBooking)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant']

@admin.register(RestaurantReview)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant']

admin.site.register(MenuCategory)
admin.site.register(Menu)

@admin.register(MenuReview)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu']

@admin.register(UserFavouriteRestaurant)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant']