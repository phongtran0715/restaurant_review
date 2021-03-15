from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from review.models import Review
from review.serializers import ReviewSerializer
import json, logging
from datetime import datetime
import pandas as pd
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from django.db.models import Q, Max, Sum
from restaurant.models import Restaurant
from django.core.paginator import (Paginator, EmptyPage,
	PageNotAnInteger, InvalidPage)

logger = logging.getLogger(__name__)

weight_scores = (1, 1.2, 1.4, 1.6, 1.8)
rating_points = (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1)
import datetime, time

# Create your views here.
@api_view(['GET'])
def api_get_review_view(request, **kwargs):
	"""
	?res_id -- restaurant id
	""" 
	if request.method == 'GET':
		page = request.data.get('page', 1)
		try:
			response = {}
			content = []
			restaurant_id = request.GET.get('res_id', 1)
			res_obj = Restaurant.objects.get(res_id=restaurant_id)
			record_data = res_obj.res_review.values("author", "rating", "weight_score", "text",
					"review_count", "source", "category", "country", "state", "created_date")
			
			paginator = Paginator(record_data, 30)
			response['total_record'] = paginator.count
			response['page'] = page
			response['total_page'] = paginator.num_pages
			response['page_size'] = 30

			if page > paginator.num_pages or page <= 0:
				response['data'] = []
			else:
				page_data = paginator.page(page)
				for item in page_data:
					content.append(item)
				response['data'] = content

			return Response(response, status=status.HTTP_200_OK)
		except Restaurant.DoesNotExist:
			response = {
				"message": "Not found review data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except PageNotAnInteger:
			response['data'] = paginator.page(1)
		except EmptyPage:
			response['data'] = paginator.page(paginator.num_pages)
		except InvalidPage:
			response = {
				"message": "Invalid page"
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

			weight_score = calculate_weight_score_view(res_obj.res_id)
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


@api_view(['POST'])
def api_get_all_restaurant_score(request, **kwargs):
	if request.method == 'POST':
		try:
			start_date = None
			end_date = None
			page = 1
			category = None
			if "start_date" in request.data:
				start_date = request.data["start_date"]
			if "end_date" in request.data:
				end_date = request.data["end_date"]
			if "page" in request.data:
				page = request.data["page"]
			if "category" in request.data:
				category = request.data["category"]

			is_and = False
			sql_query = '''SELECT distinct(res_id_id) as res_item_id, 1 id, count(*) as review_num FROM reviews '''

			if start_date is not None:
				sql_query += " WHERE created_date >= '{}'".format(start_date)
				is_and = True

			if end_date is not None:
				if is_and:
					sql_query += " AND created_date <= '{}'".format(end_date)
				else:
					sql_query += " WHERE created_date <= '{}'".format(end_date)
					is_and = True

			if category is not None:
				if is_and:
					sql_query += " AND category = '{}'".format(category)
				else:
					sql_query += " WHERE category = '{}'".format(category)
					is_and = True

			sql_query += " group by res_item_id order by review_num desc;"
			# print("query : {}".format(sql_query))

			restaurants = Review.objects.raw(sql_query)
			if len(list(restaurants)) <= 0:
				response = {
					"message": "Not found review data"
				}
				return Response(response, status=status.HTTP_404_NOT_FOUND)
			max_review = restaurants[0].review_num
			# print("max review count : {}".format(max_review))

			response = {}
			content = []
			paginator = Paginator(restaurants, 20)
			response['total_record'] = paginator.count
			response['page'] = page
			response['total_page'] = paginator.num_pages
			response['page_size'] = 20

			if page > paginator.num_pages or page <= 0:
				response['data'] = []
			else:
				page_data = paginator.page(page)
				# get maximum review count
				for item in page_data:
					weight_score = calculate_weight_score_view(item.res_item_id, start_date, end_date, category)
					accuracey = round((item.review_num / max_review) *100, 2)
					final_score = round(weight_score * accuracey / 100, 8)
					date_from , date_to = get_date_range(item.res_item_id, start_date, end_date)
					data = {
						"restaurant_id" : item.res_item_id,
						"category" : "",
						"review_number" : item.review_num,
						"accuracey" : accuracey,
						"weighted_score" : weight_score,
						"final_score" : final_score,
						"date_from" : date_from,
						"date_to" : date_to
					}
					content.append(data)
				response['data'] = content

			return Response(response, status=status.HTTP_200_OK)
		except Review.DoesNotExist:
			response = {
				"message": "Not found review data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except PageNotAnInteger:
			response['data'] = paginator.page(1)
		except EmptyPage:
			response['data'] = paginator.page(paginator.num_pages)
		except InvalidPage:
			response = {
				"message": "Invalid page"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


def calculate_weight_score_view(res_id, start_date=None, end_date=None, category=None):
	data = []
	sql_query = ''' SELECT rating, review_count, weight_score, id FROM reviews WHERE res_id_id = {} '''.format(res_id)
	if start_date is not None:
		sql_query += " AND created_date >= '{}'".format(start_date)

	if end_date is not None:
		sql_query += " AND created_date <= '{}'".format(end_date)

	if category is not None:
		sql_query += " AND category = '{}'".format(category)

	sql_query += " AND (source = 'google' OR source = 'facebook' OR source = 'opentable' OR source = 'tripadvisor' OR source = 'ubereats');"

	# print("query : {}".format(sql_query))
	review_obj = Review.objects.raw(sql_query)
	for w_score in weight_scores:
		frame_data = [0,0,0,0,0,0,0,0,0]
		for review in review_obj:
			if review.weight_score == w_score:
				index = rating_points.index(review.rating)
				frame_data[index] += 1
		data.append(frame_data)

	df = pd.DataFrame(data,columns=rating_points)
	# print(df)
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

def get_date_range(restaurant_id, start_date=None, end_date=None):
	if start_date is None:
		date_from  = Review.objects.filter(res_id_id=restaurant_id).order_by('-created_date').earliest('created_date').created_date
	else:
		date_from = start_date

	if end_date is None:
		date_to = Review.objects.filter(res_id_id=restaurant_id).order_by('-created_date').latest('created_date').created_date
	else:
		date_to = end_date
	
	return str(date_from), str(date_to)

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
	generator = schemas.SchemaGenerator(title='Rest Swagger')
	return Response(generator.get_schema(request=request))
	


	
