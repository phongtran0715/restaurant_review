from rest_framework import serializers
from review.models import Review, ScrapeReviewStatus


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ('author', 'rating', 'weight_score', 'text', 'review_count', 'source', 'category', 'country', 'state', 'created_date')

class ScrapeStatusSerilizer(serializers.ModelSerializer):
	class Meta:
		model = ScrapeReviewStatus
		fields = '__all__'