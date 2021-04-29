from django.contrib import admin
from email_scrape.models import Email

@admin.register(Email)
class RestaurantAdmin(admin.ModelAdmin):
	list_display = ("email_id", "subject", "email_from", "email_date", "email_body_text", "category")
	list_filter = ("email_from", "category", "subject")