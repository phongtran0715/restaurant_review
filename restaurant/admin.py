from django.contrib import admin
from restaurant.models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	list_display = ("res_id", "name", "number_review")
	list_filter = ("res_id", "name")