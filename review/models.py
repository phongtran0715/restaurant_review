from django.db import models

# Create your models here.
class Review(models.Model):
	author = models.CharField(max_length=128)
	rating = models.FloatField()
	weight_score = models.FloatField()
	text = models.CharField(max_length=10240)
	restaurant_id = models.IntegerField(blank=True, default=0)
	review_count = models.IntegerField(blank=True, default=0)
	source = models.CharField(max_length=128, blank=True)
	category = models.CharField(max_length=45, blank=True)
	country = models.CharField(max_length=45, blank=True)
	state = models.CharField(max_length=45, blank=True)
	created_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.author

	class Meta:
		db_table = "reviews"
		ordering = ['created_date']
