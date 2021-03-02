from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from review.models import Review
from review.serializers import ReviewSerializer
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['GET'])
def api_get_review_view(request, **kwargs):
	if request.method == 'GET':
		try:
			restaurant_id = request.GET.get('res_id', 1)
			reviews = Review.objects.filter(restaurant_id=restaurant_id)
			response = {
				"data" : reviews.values()
			}
			return Response(response, status=status.HTTP_200_OK)
		except Review.DoesNotExist:
			response = {
				"message": "Not found tracking data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_insert_review_view(request, **kwargs):
	if request.method == 'POST':
		serializer = ReviewSerializer(data=request.data)
		if serializer.is_valid():
			Review.objects.create(author=serializer.data['author'], rating=serializer.data['rating'],
				weight_score=serializer.data['weight_score'], text=serializer.data['text'],
				restaurant_id=serializer.data['restaurant_id'], review_count=serializer.data['review_count'],
				category=serializer.data['category'], country=serializer.data['country'],
				state=serializer.data['state'], created_date=serializer.data['created_date'])
			data = {
					'message' : 'Success'
				}
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_restaurant_score(request, **kwargs):
	if request.method == 'GET':
		try:
			restaurant_id = request.GET.get('res_id', 1)
			reviews = Review.objects.filter(restaurant_id=restaurant_id)
			response = {
				"restaurant_id" : restaurant_id,
				"category" : "",
				"date_range" : "",
				"review_count" : "",
				"accuracey" : "",
				"weighted_score" : "0.820338983050847",
			}
			return Response(response, status=status.HTTP_200_OK)
		except Review.DoesNotExist:
			response = {
				"message": "Not found tracking data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)
