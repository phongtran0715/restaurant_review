import ijson
import requests
from datetime import datetime


API_ENDPOINT="http://54.252.173.242:8000/api/review/new"
# API_ENDPOINT="http://127.0.0.1:8000/api/review/new/"
file_path="/home/jack/Downloads/Document/restaurant/reviews_dump.json"

'''
{"model": "reviews.review", "pk": 79920, "fields": {"author": "dtm6918", "date": "2019-07-02", "rating": 4.0, "source_url": "https://www.tripadvisor.com.au/Restaurant_Review-g255340-d756226-Reviews-Hog_s_Breath_Cafe-Toowoomba_Queensland.html", "text": "Over all was great service again just a little slow getting back for drink orders but food very good.", "source": "tripadvisor", "batch": null, "restaurant": 1939, "creation_date": "2019-07-02T00:00:00Z", "status": false, "task": "", "task_response": "", "nps_ID": "686162975", "nps_number": "", "nps_email": "", "last_updated_status": "2020-11-05T17:05:09.761Z", "last_updated_task_response": "2020-11-05T17:05:09.761Z", "last_updated_task": "2020-11-05T17:05:09.761Z", "review_removal": null, "reviewer_count": "2"}},
'''

def get_weighted_from_review(review_count):
	weighted_score = 1
	if review_count <= 5:
		weighted_score = 1
	elif review_count > 5 and review_count <= 10:
		weighted_score = 1.2
	elif review_count > 10 and review_count <= 20:
		weighted_score = 1.4
	elif review_count > 20 and review_count <= 50:
		weighted_score = 1.6
	elif review_count > 50:
		weighted_score = 1.6
	else:
		weighted_score = 1
	return str(weighted_score)


def parse_json(file_path):
	with open(file_path, 'rb') as input_file:
		objs = ijson.items(input_file, 'item')
		count = 0
		for it in objs:
			print("count : {} - restaurant_id : {}".format(count, it['fields']['restaurant']))
			review_count = it['fields']['reviewer_count']
			if review_count is None or review_count == "":
				review_count = 0
			else:
				review_count = int(review_count)
			data = {
				'author':it['fields']['author'], 
				'rating':float(it['fields']['rating']), 
				'weight_score': get_weighted_from_review(review_count), 
				'text':it['fields']['text'],
				'restaurant_id':it['fields']['restaurant'],
				'review_count':review_count,
				'source' : it['fields']['source'],
				'category':'NA',
				'country':'US',
				'state':'GA',
				'created_date': datetime.strptime(it['fields']['date'], '%Y-%m-%d')
			}
			try:
				r = requests.post(url = API_ENDPOINT, data = data)
				print("status code : {}".format(r.status_code))
				if r.status_code == 400:
					print(data)
			except requests.ConnectionError:
				print("failed to connect")
			count += 1

if __name__ == '__main__':
	parse_json(file_path)