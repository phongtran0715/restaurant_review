from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = '__all__'

class RestaurantScoreSerializer(serializers.Serializer):
	restaurant_id = serializers.IntegerField(default=0)
	category = category = serializers.CharField(max_length=45, allow_blank=True)
	review_count = serializers.IntegerField(default=0)
	accuracey = serializers.FloatField(default=0)
	weighted_score = serializers.FloatField(default=0)
	final_score = serializers.FloatField(default=0)
	date_from = serializers.DateTimeField()
	date_to = serializers.DateTimeField()

# class ScrapeReviewStatusSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = ScrapeReviewStatus
# 		# fields = '__all__'
# 		exclude = ('id', )

# 	def save(self, validated_data):
# 		return ScrapeReviewStatus.objects.create(**validated_data)