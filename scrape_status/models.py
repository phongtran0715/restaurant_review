from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class ScrapeReviewStatus(models.Model):
	error_msg = models.CharField(null=True, default="", max_length=5000)
	res_id = models.IntegerField(default=0)
	scrape_url = models.CharField(null=True, default="", max_length=512);
	retry_count = models.IntegerField(null=True, default=0)
	review_count = models.IntegerField(null=True, default=0)
	status = models.CharField(null=True,default="UNKNOW", max_length=32, db_index=True)
	platform = models.CharField(null=True,default="UNKNOW", max_length=32, db_index=True)
	created_date = models.DateTimeField(blank=False)
	last_updated_at = models.DateTimeField(blank=False)

	def __str__self():
		return "{}-{}".format(self.res_id, self.platform)

	class Meta:
		verbose_name_plural = "Status List"
		db_table = "scrape_status"
		ordering = ['res_id']