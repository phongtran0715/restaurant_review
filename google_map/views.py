from django.shortcuts import render
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from outscraper import ApiClient
from django.conf import settings
from google_map.scraper import WebDriver


@api_view(['GET'])
def api_search_google_map_view(request, *kwargs):
	if request.method == 'GET':
		response = {}
		url = "https://www.google.com/maps/search/pizza+coffe"
		x = WebDriver()
		result = x.scrape(url)
		if result is not None:
			print(x.scrape(url))
			return Response(response, status=status.HTTP_200_OK)
		else:
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)
