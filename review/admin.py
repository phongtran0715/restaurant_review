from django.contrib import admin
from review.models import Review, ScrapeReviewStatus


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Review._meta.get_fields()]
	list_filter = ("author", "res_id", "source", "category", "rating", "weight_score")
	list_per_page = 50

@admin.register(ScrapeReviewStatus)
class ScrapeReviewStatusAdmin(admin.ModelAdmin):
	list_display = ("id", "platform", "scrape_url", "status", "error_msg", "retry_count", "review_count", "view_google_link")
	list_filter = ("res_id", "retry_count", "review_count", "status", "platform")
	list_editable = ('scrape_url',)

	def view_google_link(self, obj):
		from django.utils.html import format_html
		url = "https://www.google.com/"
		return format_html('<a href="{}" target="_blank">Search</a>', url)

	view_google_link.short_description = "Google Search"