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
from django.db.models import Q
from restaurant.models import Restaurant
from django.db.models import Max

logger = logging.getLogger(__name__)

weight_scores = (1, 1.2, 1.4, 1.6, 1.8)
rating_points = (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1)

# Create your views here.
@api_view(['GET'])
def api_get_review_view(request, **kwargs):
	"""
	?res_id -- restaurant id
	""" 
	if request.method == 'GET':
		try:
			restaurant_id = request.GET.get('res_id', 1)
			res_obj = Restaurant.objects.get(res_id=restaurant_id)
			response = {
				"data" : res_obj.res_review.values("author", "rating", "weight_score", "text",
					"review_count", "source", "category", "country", "state", "created_date")
			}
			return Response(response, status=status.HTTP_200_OK)
		except Restaurant.DoesNotExist:
			response = {
				"message": "Not found review data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_insert_review_view(request, **kwargs):
	"""
	"author" : "author_name",
	"rating" : "1",
	"weight_score" : "1",
	"text" : "content",
	"restaurant_id" : "1",
	"review_count" : "30",
	"source" : "google",
	"category" : "Pizza",
	"country" : "United States",
	"state" :"GA",
	"created_date" : "2021-01-18"
	"""
	if request.method == 'POST':
		serializer = ReviewSerializer(data=request.data)
		if serializer.is_valid():
			# TODO: check if request missing restaurant id
			try:
				res_obj = Restaurant.objects.get(res_id=request.data['restaurant_id'])
			except Restaurant.DoesNotExist:
				res_obj = Restaurant(res_id=request.data['restaurant_id'], name='', number_review=0)
				res_obj.save()

			review = res_obj.res_review.create(author=serializer.data['author'], rating=serializer.data['rating'],
				weight_score=serializer.data['weight_score'], text=serializer.data['text'], review_count=serializer.data['review_count'],
				source=serializer.data['source'], category=serializer.data['category'], country=serializer.data['country'],
				state=serializer.data['state'], created_date=serializer.data['created_date'])
			review.save()

			res_obj.number_review = int(res_obj.number_review) + 1
			res_obj.save()
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
	"""
	?res_id -- restaurant id
	""" 
	if request.method == 'GET':
		try:
			# get maximum review count
			try:
				res_obj = Restaurant.objects.get(res_id=request.GET.get('res_id'))
			except Restaurant.DoesNotExist:
				response = {
					"message": "Not found review data"
				}
				return Response(response, status=status.HTTP_404_NOT_FOUND)

			max_review = Restaurant.objects.aggregate(Max('number_review'))['number_review__max']
			print("Maximum review : {}".format(max_review))

			weight_score = calculate_weight_score_view(res_obj.res_review)
			accuracey = round((res_obj.number_review / max_review) *100, 2)
			final_score = round(weight_score * accuracey / 100, 8)
			date_from , date_to = get_date_range(res_obj.id)

			response = {
				"restaurant_id" : res_obj.res_id,
				"category" : "",
				"review_count" : res_obj.number_review,
				"accuracey" : accuracey,
				"weighted_score" : weight_score,
				"final_score" : final_score,
				"date_from" : date_from,
				"date_to" : date_to
			}
			return Response(response, status=status.HTTP_200_OK)
		except Review.DoesNotExist:
			response = {
				"message": "Not found review data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_all_restaurant_score(request, **kwargs):
	if request.method == 'GET':
		try:
			response = {}
			result = []
			restaurants = Restaurant.objects.all()
			response['total'] = Restaurant.objects.all().count()
			# get maximum review count
			max_review = Restaurant.objects.all().order_by('-number_review').latest('number_review')
			print("Maximum review : {}".format(max_review))

			for res in restaurants:
				weight_score = calculate_weight_score_view(res.res_id)
				accuracey = round((res.number_review / max_review) *100, 2)
				final_score = round(weight_score * accuracey / 100, 8)
				date_from , date_to = get_date_range(res.res_id)

				data = {
					"restaurant_id" : res.res_id,
					"category" : "",
					"review_count" : res.number_review,
					"accuracey" : accuracey,
					"weighted_score" : weight_score,
					"final_score" : final_score,
					"date_from" : date_from,
					"date_to" : date_to
				}
				result.append(data)
			response['data'] = result
			return Response(response, status=status.HTTP_200_OK)
		except Review.DoesNotExist:
			response = {
				"message": "Not found review data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


def calculate_weight_score_view(res_review):
	data = []
	for w_score in weight_scores:
		frame_data = [0,0,0,0,0,0,0,0,0]
		for review in res_review.all():
			if review.weight_score == w_score and review.source in ("google", "facebook", "opentable", "tripadvisor", "ubereats") :
				if review.rating in rating_points:
					index = rating_points.index(review.rating)
					frame_data[index] += 1
		data.append(frame_data)
		
		# items = Review.objects.filter(Q(restaurant_id=restaurant_id) & Q(weight_score=w_score) 
		# 	& (Q(source='google') | Q(source='facebook') | Q(source='opentable') | Q(source='tripadvisor') | Q(source='ubereats')))
		# for item in items:
		# 	if item.rating in rating_points:
		# 		index = rating_points.index(item.rating)
		# 		frame_data[index] += 1
		# data.append(frame_data)

	df = pd.DataFrame(data,columns=rating_points)
	print(df)
	total_point = 0.0
	sum_rows = df.sum(axis=1)
	for index in range (0, len(weight_scores)):
		total_point += weight_scores[index] * sum_rows[index]

	if total_point > 0.0:
		res_score = 0.0
		for (columnName, columnData) in df.iteritems():
			sum_per_col = 0.0
			for col_index in range(0, len(columnData)):
				sum_per_col += columnData[col_index] * weight_scores[col_index]
			sum_per_col = (sum_per_col / total_point) / 5.0 * float(columnName)
			res_score += sum_per_col
	else:
		res_score = 0.0
	return round(res_score, 8)

def get_date_range(restaurant_id):
	date_to = Review.objects.filter(res_id_id=restaurant_id).order_by('-created_date').latest('created_date')
	date_from  = Review.objects.filter(res_id_id=restaurant_id).order_by('-created_date').earliest('created_date')
	return str(date_from.created_date), str(date_to.created_date)

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
	generator = schemas.SchemaGenerator(title='Rest Swagger')
	return Response(generator.get_schema(request=request))
	


	
