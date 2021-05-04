from django.shortcuts import render
import logging
import time, os, re
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.conf import settings
from google_map.scraper import WebDriver
from googlesearch.googlesearch import GoogleSearch


# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

class SearchGoogleMapView(generics.ListAPIView):
	def list(self, request):
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

class SearchGoogleView(generics.ListAPIView):
	def list(self, request):
		response = {}
		data = []
		keyword = request.GET.get('keyword')
		keyword = keyword.replace(" ", "+")
		count, titles, urls = GoogleSearch().search_selenium(query=keyword)
		print(count.text)
		total = int(re.sub("[', ]", "", re.search("(([0-9]+[', ])*[0-9]+)", count.text).group(1)))
		response['total_result'] = total
		for i in range(len(titles)):
			data.append({
				'title' : titles[i].text,
				'url' : urls[1].get_attribute('href'),
				})
		response['data'] = data
		return Response(response, status=status.HTTP_200_OK)