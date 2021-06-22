from django.db import models
from user.models import User
from datetime import datetime


class Restaurant(models.Model):
	res_id = models.IntegerField(default=0, db_index=True, unique=True)
	number_review = models.IntegerField(default=0)

	def __str__(self):
		return "{}".format(self.res_id)

	class Meta:
		db_table = "restaurant"
		ordering = ['res_id']

class WebsitePerformance(models.Model):
	user_id = models.IntegerField(default=0)
	company_website = models.URLField(('company website'), blank=True,null=True)
	performance = models.IntegerField(default=0)
	accessibility = models.IntegerField(default=0)
	best_practices = models.IntegerField(default=0)
	seo = models.IntegerField(default=0)
	first_contentful_paint = models.FloatField(default=0.0)
	speed_index = models.FloatField(default=0.0)
	interactive = models.FloatField(default=0.0)
	largest_contentful_paint = models.FloatField(default=0.0)
	total_blocking_time = models.FloatField(default=0.0)
	cumulative_layout_shift = models.FloatField(default=0.0)
	last_updated_at = models.DateTimeField(blank=False,default=datetime.strptime("1970-01-01", "%Y-%m-%d").date())

	class Meta:
		db_table = "website_benchmark"
