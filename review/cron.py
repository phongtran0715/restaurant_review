import datetime
import logging
from review.models import Review, ScoreMonth, ScoreQuarter, ScoreYear
from review.views import calculate_weight_score_view
from django.db.models import Max, Min, Sum, Q
import pandas as pd


logger = logging.getLogger(__name__)
weight_scores = (1, 1.2, 1.4, 1.6, 1.8)
rating_points = (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1)

def build_restaurant_resource():
	print("Start cron job : {}".format(datetime.datetime.now()))
	end_date = Review.objects.aggregate(Max('created_date'))['created_date__max']
	start_date = Review.objects.aggregate(Min('created_date'))['created_date__min']
	for year in range(start_date.year, end_date.year + 1):
		# calculate score in this YEAR
		update_score_by_period(datetime.date(year, 1, 1), 'year')
			
		# calculate score each QUATER in year
		for quater in range(1,5):
			update_score_by_period(datetime.date(year, quater, 1), 'quater')

		# calculate scrore each MONTH in year
		for month in range(1,13):
			update_score_by_period(datetime.date(year, month, 1), 'month')
	print("End cron job : {}".format(datetime.datetime.now()))
	pass

def update_score_by_period(period_value, period_type=None):
	is_and = False
	sql_query = '''SELECT distinct(res_id_id) as res_item_id, 1 id, count(*) as review_num FROM reviews '''
	if period_type == 'year':
		sql_query += " WHERE YEAR(created_date) = {} ".format(period_value.year)
	elif period_type == 'month':
		sql_query += " WHERE YEAR(created_date) = {} AND MONTH(created_date) = {}".format(period_value.year, period_value.month)
	elif period_type == 'quater':
		quater_value = period_value.month
		quater_list = (1,2,3,4)
		if quater_value == 1:
			quater_list = (1,2,3)
		elif quater_value == 2:
			quater_list = (4,5,6)
		elif quater_value == 3:
			quater_list = (7,8,9)
		elif quater_value == 4:
			quater_list = (10,11,12)

		sql_query += """ WHERE YEAR(created_date) = {} AND MONTH(created_date) = {} 
		AND MONTH(created_date) = {} AND MONTH(created_date) = {} """.format(period_value.year, quater_list[0], quater_list[1], quater_list[2])
	
	sql_query += " GROUP BY res_item_id ORDER BY review_num DESC;"

	restaurants = Review.objects.raw(sql_query)
	if len(list(restaurants)) <= 0:
		return
	max_review = restaurants[0].review_num

	for item in restaurants:
		weight_score = calculate_weight_score_view(item.res_item_id, period_value, period_type)
		accuracey = round((item.review_num / max_review) *100, 2)
		final_score = round(weight_score * accuracey / 100, 8)
		if period_type == 'month':
			obj, created = ScoreMonth.objects.filter(Q(res_id=item.res_item_id), Q(period=datetime.date(period_value.year, period_value.month, 1))).get_or_create(res_id=item.res_item_id, accuracey=accuracey, final_score=final_score, period=datetime.date(period_value.year, period_value.month, 1))
			if created == False:
				obj = ScoreMonth(res_id=item.res_item_id, accuracey=accuracey, final_score=final_score, period=datetime.date(period_value.year, period_value.month, 1))
				obj.save()
		elif period_type == 'quater':
			obj, created = ScoreQuarter.objects.filter(Q(res_id=item.res_item_id), Q(period=datetime.date(period_value.year, period_value.month, 1))).get_or_create(res_id=item.res_item_id, accuracey=accuracey, final_score=final_score, period=datetime.date(period_value.year, period_value.month, 1))
			if created == False:
				obj = ScoreQuarter(res_id=item.res_item_id, accuracey=accuracey, final_score=final_score, period=datetime.date(period_value.year, period_value.month, 1))
				obj.save()
		elif period_type == 'year':
			obj, created = ScoreYear.objects.filter(Q(res_id=item.res_item_id), Q(period=datetime.date(period_value.year, 1, 1))).get_or_create(res_id=item.res_item_id, accuracey=accuracey, final_score=final_score, period=datetime.date(period_value.year, 1, 1))
			if created == False:
				obj = ScoreYear(res_id=item.res_item_id, accuracey=accuracey, final_score=final_score, period=datetime.date(period_value.year, 1, 1))
				obj.save()

def calculate_weight_score_view(res_id, period_value, period_type):
	data = []
	sql_query = ''' SELECT rating, review_count, weight_score, id FROM reviews WHERE res_id_id = {} '''.format(res_id)
	if period_type == 'year':
		sql_query += " AND YEAR(created_date) = {} ".format(period_value.year)
	elif period_type == 'month':
		sql_query += " AND YEAR(created_date) = {} AND MONTH(created_date) = {} ".format(period_value.year, period_value.month)
	elif period_type == 'quater':
		quater_value = period_value.month
		quater_list = (1,2,3,4)
		if quater_value == 1:
			quater_list = (1,2,3)
		elif quater_value == 2:
			quater_list = (4,5,6)
		elif quater_value == 3:
			quater_list = (7,8,9)
		elif quater_value == 4:
			quater_list = (10,11,12)

		sql_query += """ AND YEAR(created_date) = {} AND MONTH(created_date) = {} 
		AND MONTH(created_date) = {} AND MONTH(created_date) = {} """.format(period_value.year, quater_list[0], quater_list[1], quater_list[2])

	sql_query += " AND (source = 'google' OR source = 'facebook' OR source = 'opentable' OR source = 'tripadvisor' OR source = 'ubereats');"
	print("sql_query : {}".format(sql_query))

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
		
