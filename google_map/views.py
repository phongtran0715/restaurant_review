from django.shortcuts import render
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from google_map.scraper import WebDriver
import time


@api_view(['GET'])
def api_search_google_map_view(request, *kwargs):
	if request.method == 'GET':
		response = {}
		data = []
		keyword = request.GET.get('keyword')
		keyword = keyword.replace(" ", "+")
		url = "https://www.google.com/maps/search/{}".format(keyword)
		print("Keyword : {}".format(keyword))
		driver = WebDriver()
		links, locations_name, categories = driver.get_all_location_link(url)
		for x in range(0,len(links)):
			location_data = {
				'location_name' : locations_name[x],
				'category' : categories[x],
			}
			data.append(location_data)
		response['data'] = data	
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)
