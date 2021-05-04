from rest_framework import serializers
from review.models import Review, ScrapeReviewStatus


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = '__all__'

class ScrapeReviewStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScrapeReviewStatus
		fields = '__all__'
		# exclude = ('id', )

	def save(self, validated_data):
		return ScrapeReviewStatus.objects.create(**validated_data)