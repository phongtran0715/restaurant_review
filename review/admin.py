from django.contrib import admin
from review.models import Review, ScoreMonth, ScoreQuarter, ScoreYear
from django.utils.html import format_html
from restaurant.models import Restaurant


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Review._meta.get_fields()]
	list_filter = ("author", "res_id", "source", "category", "rating", "weight_score")
	list_per_page = 50

@admin.register(ScoreMonth)
class ScoreMonthAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ScoreMonth._meta.get_fields()]
	list_filter = ("res_id", "review_count", "accuracey", "weight_score", "final_score")
	list_per_page = 50

@admin.register(ScoreQuarter)
class ScoreQuarterAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ScoreQuarter._meta.get_fields()]
	list_filter = ("res_id", "review_count", "accuracey", "weight_score", "final_score")
	list_per_page = 50

@admin.register(ScoreYear)
class ScoreYearAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ScoreYear._meta.get_fields()]
	list_filter = ("res_id", "review_count", "accuracey", "weight_score", "final_score")
	list_per_page = 50
