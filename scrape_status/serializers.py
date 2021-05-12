from rest_framework import serializers
from scrape_status.models import ScrapeReviewStatus


class ScrapeReviewStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScrapeReviewStatus
		fields = '__all__'

	def save(self, validated_data):
		return ScrapeReviewStatus.objects.create(**validated_data)