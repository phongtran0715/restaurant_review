from django.db import models

# Create your models here.
class Restaurant(models.Model):
	res_id = models.IntegerField(default=0, db_index=True)
	name = models.CharField(max_length=128, blank=True)
	number_review = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	class Meta:
		db_table = "restaurant"
		ordering = ['res_id']

class Platform(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=128, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = "platform"

	