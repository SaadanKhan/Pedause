from django.contrib import admin
from .models import *


@admin.register(UserFavouriteFood)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'food']

@admin.register(CartItem)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'food']

admin.site.register(Cart)
admin.site.register(FoodCategory)
admin.site.register(Food)
