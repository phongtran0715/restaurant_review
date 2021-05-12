from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import ScrapeReviewStatusSerializer


@api_view(['POST'])
def import_scrape_status(request, **kwargs):
	if request.method == 'POST':
		data = request.data
		serializer = ScrapeReviewStatusSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(serializer.validated_data)
			return Response(status=status.HTTP_200_OK)
		else:
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)
