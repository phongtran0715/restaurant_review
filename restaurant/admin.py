from django.contrib import admin
from restaurant.models import Restaurant, Platform


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Restaurant._meta.get_fields()]
	list_filter = ("res_id", "name")

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
	list_display = ("id", "name")