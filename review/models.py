from django.db import models
from restaurant.models import Restaurant, Platform
from django.utils.html import format_html
from django.shortcuts import redirect, reverse


class Review(models.Model):
	author = models.CharField(max_length=128)
	rating = models.FloatField()
	weight_score = models.FloatField(db_index=True)
	text = models.TextField(blank=True)
	review_count = models.IntegerField(blank=True, default=0)
	source = models.CharField(max_length=128, blank=True)
	category = models.CharField(max_length=45, blank=True)
	country = models.CharField(max_length=45, blank=True)
	state = models.CharField(max_length=45, blank=True)
	created_date = models.DateField(blank=True, null=True, db_index=True)
	res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_review', help_text="Name of the restaurant")

	def __str__(self):
		return self.author

	class Meta:
		db_table = "reviews"
		ordering = ['created_date']

class ScoreMonth(models.Model):
	res_id = models.IntegerField(default=0, blank=False,db_index=True)
	review_count = models.IntegerField(blank=True, default=0)
	accuracey = models.IntegerField(default=0, blank=False)
	weight_score = models.FloatField(default=0.0, blank=False)
	final_score = models.FloatField(default=0.0, blank=False)
	period = models.DateField(blank=True, null=True, db_index=True)

	def __str__(self):
		return self.res_id

	class Meta:
		db_table = "scores_month"
		ordering = ['final_score']

class ScoreQuarter(models.Model):
	res_id = models.IntegerField(default=0, blank=False,db_index=True)
	review_count = models.IntegerField(blank=True, default=0)
	accuracey = models.IntegerField(default=0, blank=False)
	weight_score = models.FloatField(default=0.0, blank=False)
	final_score = models.FloatField(default=0.0, blank=False)
	period = models.DateField(blank=True, null=True, db_index=True)

	def __str__(self):
		return self.res_id

	class Meta:
		db_table = "scores_quarter"
		ordering = ['final_score']

class ScoreYear(models.Model):
	res_id = models.IntegerField(default=0, blank=False,db_index=True)
	review_count = models.IntegerField(blank=True, default=0)
	accuracey = models.IntegerField(default=0, blank=False)
	weight_score = models.FloatField(default=0.0, blank=False)
	final_score = models.FloatField(default=0.0, blank=False)
	period = models.DateField(blank=True, null=True, db_index=True)

	def __str__(self):
		return self.res_id

	class Meta:
		db_table = "scores_year"
		ordering = ['final_score']

# class ScrapeReviewStatus(models.Model):
# 	error_msg = models.CharField(blank=True, default="", max_length=1024)
# 	res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_scrape', db_index=True)
# 	scrape_url = models.CharField(blank=True, default="", max_length=512);
# 	retry_count = models.IntegerField(default=0)
# 	review_count = models.IntegerField(default=0)
# 	status = models.CharField(blank=False, default="UNKNOW", max_length=32, db_index=True)
# 	platform = models.CharField(blank=False, default="UNKNOW", max_length=32, db_index=True)
# 	created_date = models.DateTimeField(blank=False, auto_now_add=True)
# 	last_updated_at = models.DateTimeField(blank=False, auto_now_add=True)

# 	def __str__self():
# 		return "{}-{}".format(self.res_id, self.platform)

# 	class Meta:
# 		db_table = "scrape_status"
# 		ordering = ['res_id']

# 	def update_url_link(self):
# 		change_url = reverse('admin:restaurant_restaurant_change', args=(self.res_id,))
# 		return format_html('<a href="{}" target="_blank">Edit</a>', change_url)
# 	update_url_link.short_description = "Update URL"

