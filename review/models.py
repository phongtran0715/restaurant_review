from django.db import models
from restaurant.models import Restaurant
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
	res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='res_review', to_field='res_id', help_text="Restaurant ID")

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

