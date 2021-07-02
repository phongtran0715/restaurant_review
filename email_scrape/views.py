from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from email_scrape.models import Email
from email_scrape.serializers import EmailSerializer
import logging, json
from datetime import datetime

logger = logging.getLogger(__name__)


class EmailListView(generics.ListCreateAPIView):
	"""
    Returns a list of scraped email in the system.
    ---
    parameters:
    - name: subject
      description: Email subject
      required: false
      type: string
      paramType: form
    - name: category
      description: Email category
      paramType: form
      required: false
      type: string

    """
	queryset = Email.objects.all()
	serializer_class = EmailSerializer
	filterset_fields = ['subject', 'email_from', 'category']

	def list(self, request):
		queryset = self.get_queryset()
		category = self.request.query_params.get('category')
		subject = self.request.query_params.get('subject')
		email_from = self.request.query_params.get('email_from')
		date_from = self.request.query_params.get('date_from')
		date_to = self.request.query_params.get('date_to')

		if category is not None and category != "":
			queryset = queryset.filter(email_from__contains="+{}+".format(category))
		if subject is not None and subject != "":
			queryset = queryset.filter(subject__contains="{}".format(subject))
		if email_from is not None and email_from != "":
			queryset = queryset.filter(email_from__exact="{}".format(email_from))
		if date_from is not None and date_from != "":
			queryset = queryset.filter(email_date__gte="{}".format(datetime.strptime(date_from, '%y-%m-%d')))
		if date_to is not None and date_to != "":
			queryset = queryset.filter(email_date__lte="{}".format(datetime.strptime(date_to, '%y-%m-%d')))

		serializer = EmailSerializer(queryset, many=True)
		return Response(serializer.data)

class EmailDetailView(generics.RetrieveAPIView):
	"""
    Returns an email detail information.

    """
	queryset = Email.objects.all()
	serializer_class = EmailSerializer
	pagination_class = None

class EmailSenderListView(generics.ListAPIView):
	"""
    Returns list sender email.

    """
	queryset = Email.objects.values('email_from').distinct()
	serializer_class = EmailSerializer

	def list(self, request):
		queryset = self.get_queryset()
		serializer = EmailSerializer(queryset, many=True)
		response = {}
		email_data = []
		for it in serializer.data:
			email_count = Email.objects.filter(email_from=it['email_from']).count()
			email_data.append({
				"email_from" : it['email_from'],
				"count" : email_count
			})
		response["data"] = email_data
		return Response(response)