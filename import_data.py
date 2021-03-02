import pandas as pd
import requests 


API_ENDPOINT="http://127.0.0.1:8000/api/v1/review/new/"
file_path="/home/jack/Downloads/restaurant/Requirement_2.xlsx"
df = pd.read_excel (file_path, engine='openpyxl')
for index, row in df.iterrows():
	data = {
		'author':row[0], 
		'rating':row[2], 
		'weight_score':row[3], 
		'text':row[4],
		'restaurant_id':row[5],
		'review_count':row[6],
		'category':row[7],
		'country':row[8],
		'state':row[9],
		'created_date':row[1].strftime('%Y-%m-%d'),
	} 
	try:
		r = requests.post(url = API_ENDPOINT, data = data)
		print("row : {} - status code : {} - response : {}".format(index, r.status_code, r.text))
	except requests.ConnectionError:
		print("failed to connect")