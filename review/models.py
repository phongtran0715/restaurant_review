from django.db import models
from restaurant.models import Restaurant

# Create your models here.
class Review(models.Model):
	author = models.CharField(max_length=128)
	rating = models.FloatField()
	weight_score = models.FloatField(db_index=True)
	text = models.CharField(max_length=10240, blank=True)
	review_count = models.IntegerField(blank=True, default=0)
	source = models.CharField(max_length=128, blank=True)
	category = models.CharField(max_length=45, blank=True)
	country = models.CharField(max_length=45, blank=True)
	state = models.CharField(max_length=45, blank=True)
	created_date = models.DateField(blank=True, null=True, db_index=True)
	res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_review')

	def __str__(self):
		return self.author

	class Meta:
		db_table = "reviews"
		ordering = ['created_date']
