from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ('author', 'rating', 'weight_score', 'text', 'review_count', 'source', 'category', 'country', 'state', 'created_date')