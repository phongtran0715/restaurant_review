import pandas as pd
import requests 


# API_ENDPOINT="http://54.252.173.242:8000/api/review/new/"
API_ENDPOINT="http://127.0.0.1:8000/api/review/new/"
file_path="/home/jack/Downloads/restaurant/Requirement_3.xlsx"
df = pd.read_excel (file_path, engine='openpyxl')
for index, row in df.iterrows():
	data = {
		'author':row[12], 
		'rating':row[14], 
		'weight_score':row[15], 
		'text':row[16],
		'restaurant_id':row[17],
		'review_count':row[18],
		'source' : row[19],
		'category':row[20],
		'country':row[21],
		'state':row[22],
		'created_date':row[13].strftime('%Y-%m-%d'),
	} 
	try:
		r = requests.post(url = API_ENDPOINT, data = data)
		print("row : {} - id - {} - status code : {} - response : {}".format(index, row[17], r.status_code, r.text))
	except requests.ConnectionError:
		print("failed to connect")