from django.shortcuts import render
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from google_map.scraper import WebDriver
import time, os
from googlesearch.googlesearch import GoogleSearch


# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

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


@api_view(['GET'])
def api_search_google_search_view(request, *kwargs):
	if request.method == 'GET':
		response = {}
		data = []
		keyword = request.GET.get('keyword')
		keyword = keyword.replace(" ", "+")
		search_data = GoogleSearch().search(query=keyword, prefetch_pages=True)
		response['total_result'] = search_data.total
		for result in search_data.results:
			data.append({
				'title' : result.title,
				'url' : result.url,
				# 'content' : result.get_text().strip()
				})
		response['data'] = data
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


