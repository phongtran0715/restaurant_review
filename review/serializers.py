from rest_framework import serializers
from review.models import Review, ScrapeReviewStatus


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = '__all__'

class ScrapeStatusSerilizer(serializers.ModelSerializer):
	class Meta:
		model = ScrapeReviewStatus
		fields = '__all__'