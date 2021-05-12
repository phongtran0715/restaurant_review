from django.contrib import admin
from .models import ScrapeReviewStatus


@admin.register(ScrapeReviewStatus)
class ScrapeReviewStatusAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ScrapeReviewStatus._meta.fields if field.name != "id"]
