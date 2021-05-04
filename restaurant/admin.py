from django.contrib import admin
from restaurant.models import Restaurant, Platform


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	list_display = ("res_id", "name", "number_review")
	list_filter = ("res_id", "name")

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
	list_display = ("id", "name")