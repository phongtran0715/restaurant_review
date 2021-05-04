import ijson
import json
import requests
from datetime import datetime


# API_ENDPOINT="http://54.252.173.242:8000/api/review/new/"
API_ENDPOINT="http://54.252.173.242:8000/api/import_scrape_review/"
file_path="/home/jack/Downloads/Document/restaurant/reviews_dump.json"

def parse_json(file_path):
	with open(file_path, 'rb') as input_file:
		review_objs = json.load(input_file)
		count = 0
		for it in review_objs:
			print("count : {}".format(count))
			fields = it['fields']
			task_response = ""
			if 'task_response' in fields:
				task_response = fields['task_response']

			reviewer_count = 0
			if 'reviewer_count' in fields and fields['reviewer_count'] != '':
				reviewer_count = fields['reviewer_count']

			data = {
				'error_msg' : task_response,
				'res_id' : fields['restaurant'],
				'scrape_url' : fields['source_url'],
				'retry_count' : 0,
				'review_count' : reviewer_count,
				'status' : fields['status'],
				'platform' : fields['source'],
				'created_date' : fields['creation_date'],
				'last_update_date' : fields['last_updated_task'],
			}
			try:
				r = requests.post(url = API_ENDPOINT, data = data)
				print("status code : {}".format(r.status_code))
				if r.status_code != 200:
					print(r.content)
			except requests.ConnectionError:
				print("failed to connect")
			count += 1

if __name__ == '__main__':
	parse_json(file_path)