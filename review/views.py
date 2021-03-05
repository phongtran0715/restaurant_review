from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from review.models import Review
from review.serializers import ReviewSerializer
import json
import logging
from datetime import datetime
import pandas as pd
from django.db.models import Sum
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

logger = logging.getLogger(__name__)

weight_scores = (1, 1.2, 1.4, 1.6, 1.8)
rating_points = (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1)

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
			weight_score = calculate_weight_score_view(restaurant_id)
			accuracey = get_review_accuracey(restaurant_id)
			final_score = weight_score * accuracey / 100
			date_from , date_to = get_date_range(restaurant_id)

			response = {
				"restaurant_id" : restaurant_id,
				"category" : "",
				"review_count" : get_review_count(restaurant_id),
				"accuracey" : accuracey,
				"weighted_score" : weight_score,
				"final_score" : final_score,
				"date_from" : date_from,
				"date_to" : date_to
			}
			return Response(response, status=status.HTTP_200_OK)
		except Review.DoesNotExist:
			response = {
				"message": "Not found tracking data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


def calculate_weight_score_view(restaurant_id):
	data = []
	for w_score in weight_scores:
		frame_data = [0,0,0,0,0,0,0,0,0]
		items = Review.objects.filter(restaurant_id=restaurant_id, weight_score=w_score)
		for item in items:
			if item.rating in rating_points:
				index = rating_points.index(item.rating)
				frame_data[index] += 1
		data.append(frame_data)

	df = pd.DataFrame(data,columns=rating_points)
	print(df)
	# for (columnName, columnData) in df.iteritems():
	# 	print(type(columnData))
	# calculate total point 
	total_point = 0.0
	sum_rows = df.sum(axis=1)
	for index in range (0, len(weight_scores)):
		total_point += weight_scores[index] * sum_rows[index]
	print("total point : {}".format(total_point))

	if total_point > 0.0:
		res_score = 0.0
		for (columnName, columnData) in df.iteritems():
			sum_per_col = 0.0
			for col_index in range(0, len(columnData)):
				sum_per_col += columnData[col_index] * weight_scores[col_index]
			print('colm name : {}'.format(float(columnName)))
			sum_per_col = (sum_per_col / total_point) / 5.0 * float(columnName)
			res_score += sum_per_col
	else:
		res_score = 0.0
	print("res_score: {}".format(round(res_score, 8)))
	return res_score
	

def get_review_count(restaurant_id):
	item = Review.objects.filter(restaurant_id=restaurant_id).aggregate(Sum('review_count'))
	if item['review_count__sum'] is None:
		return 0
	else:
		return item['review_count__sum']

def get_review_accuracey(restaurant_id):
	# get total review
	total_record = Review.objects.filter().count()
	print("total record : {}".format(total_record))

	total_review_count = Review.objects.filter().aggregate(Sum('review_count'))['review_count__sum']
	print("total review : {}".format(total_review_count))

	res_review_count = Review.objects.filter(restaurant_id=restaurant_id).aggregate(Sum('review_count'))['review_count__sum']

	if res_review_count is None or total_review_count is None or total_review_count == 0:
		accuracey = 0
	else:
		accuracey = res_review_count / (total_review_count / total_record)
	print('accuracey : {}'.format(round(accuracey, 2)))
	return round(accuracey, 2)

def get_date_range(restaurant_id):
	date_to = Review.objects.filter(restaurant_id=restaurant_id).order_by('-created_date').latest('created_date')
	date_from  = Review.objects.filter(restaurant_id=restaurant_id).order_by('-created_date').earliest('created_date')
	return str(date_from.created_date), str(date_to.created_date)

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
	generator = schemas.SchemaGenerator(title='Rest Swagger')
	return Response(generator.get_schema(request=request))
	


	
