from rest_framework import serializers
from restaurant.models import Restaurant


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Restaurant
		fields = ('res_id', 'name', 'number_review')