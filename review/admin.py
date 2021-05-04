from django.contrib import admin
from review.models import Review, ScrapeReviewStatus
from django.utils.html import format_html
from restaurant.models import Restaurant


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Review._meta.get_fields()]
	list_filter = ("author", "res_id", "source", "category", "rating", "weight_score")
	list_per_page = 50

@admin.register(ScrapeReviewStatus)
class ScrapeReviewStatusAdmin(admin.ModelAdmin):
	list_display = ("id", "platform", "scrape_url", "status", "error_msg",
		"retry_count", "review_count", "res_id", "view_google_link", "update_url_link")
	list_filter = ("res_id", "retry_count", "review_count", "status", "platform")
	list_editable = ('scrape_url',)

	def view_google_link(self, obj):
		search_term = ""
		res_obj = Restaurant.objects.get(res_id=obj.id)
		if res_obj is not None:
			res_name = res_obj.name
			if res_name is not None:
				search_term += res_name

		if search_term != "":
			search_term += "+".format(obj.platform)
		else:
			search_term += obj.platform

		url = "https://www.google.com/search?q={}".format(search_term)
		return format_html('<a href="{}" target="_blank">Search</a>', url)

	view_google_link.short_description = "Google Search"
