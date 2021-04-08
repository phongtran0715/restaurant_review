from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import (Paginator, EmptyPage,
	PageNotAnInteger, InvalidPage)
from email_scrape.models import Email
from email_scrape.serializers import EmailSerializer
import logging, json


logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_email_view(request, **kwargs):
	if request.method == 'GET':
		category = request.GET.get('category')
		email_subject = request.GET.get('subject')
		email_from = request.GET.get('email_from')
		date_from = request.GET.get('date_from')
		date_to = request.GET.get('date_to')
		
		page = request.data.get('page', 1)
		try:
			response = {}
			content = []
			email_data = Email.objects.filter()
			if email_subject is not None:
				email_data = email_data.filter(subject__icontains=email_subject)
			if email_from is not None:
				email_data = email_data.filter(email_from__exact=email_from)
			if date_from is not None:
				email_data = email_data.filter(email_date__gte=date_from)
			if date_to is not None:
				email_data = email_data.filter(email_date__lte=date_to)
			if category is not None:
				email_data = email_data.filter(category__exact=category)

			email_data = email_data.order_by('-email_date')
			paginator = Paginator(email_data, 30)
			response['total_record'] = paginator.count
			response['page'] = page
			response['total_page'] = paginator.num_pages
			response['page_size'] = 30
			if page > paginator.num_pages or page <= 0:
				response['data'] = []
			else:
				page_data = paginator.page(page)
				for item in page_data:
					serializer = EmailSerializer(item)
					content.append(serializer.data)
				response['data'] = content
			return Response(response, status=status.HTTP_200_OK)
		except Email.DoesNotExist:
			response = {
				"message": "Not found email data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except PageNotAnInteger:
			response['data'] = paginator.page(1)
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except EmptyPage:
			response['data'] = paginator.page(paginator.num_pages)
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except InvalidPage:
			response = {
				"message": "Invalid page"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_sender_view(request, **kwargs):
	if request.method == 'GET':
		page = request.data.get('page', 1)
		try:
			response = {}
			content = []
			# email_data = Email.objects.values('email_from').distinct()
			email_data = Email.objects.raw('SELECT 1 as id, COUNT(*) as count, email_from from email_scrape WHERE YEAR(email_date) = YEAR(CURRENT_TIMESTAMP) group by email_from order by count desc')
			paginator = Paginator(email_data, 10)
			response['total_record'] = paginator.count
			response['page'] = page
			response['total_page'] = paginator.num_pages
			response['page_size'] = 10
			if page > paginator.num_pages or page <= 0:
				response['data'] = []
			else:
				page_data = paginator.page(page)
				for item in page_data:
					content.append({
						'email_from' : item.email_from,
						'number_email' : item.count
						})
				response['data'] = content
			return Response(response, status=status.HTTP_200_OK)
		except Email.DoesNotExist:
			response = {
				"message": "Not found email data"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except PageNotAnInteger:
			response['data'] = paginator.page(1)
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except EmptyPage:
			response['data'] = paginator.page(paginator.num_pages)
			return Response(response, status=status.HTTP_404_NOT_FOUND)
		except InvalidPage:
			response = {
				"message": "Invalid page"
			}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)		