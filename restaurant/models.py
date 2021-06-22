from django.db import models

# Create your models here.
class Restaurant(models.Model):
	res_id = models.IntegerField(default=0, db_index=True, unique=True)
	number_review = models.IntegerField(default=0)

	def __str__(self):
		return "{}".format(self.res_id)

	class Meta:
		db_table = "restaurant"
		ordering = ['res_id']

	