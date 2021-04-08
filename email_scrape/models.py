from django.db import models

# Create your models here.

class Email(models.Model):
	email_id = models.IntegerField(default=0)
	subject = models.CharField(max_length=4096, blank=True)
	email_from = models.EmailField(max_length=254, blank=True, db_index=True)
	email_date = models.DateTimeField(blank=True, db_index=True)
	email_body_text = models.TextField(max_length=40960, blank=True)
	email_body_html = models.TextField(max_length=40960, blank=True)
	category = models.CharField(max_length=512, blank=True)

	def __str__(self):
		return self.email_from + " - " + self.subject

	class Meta:
		db_table = "email_scrape"
		ordering = ["email_date"]