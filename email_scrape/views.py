from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from email_scrape.models import Email
from email_scrape.serializers import EmailSerializer
import logging, json

logger = logging.getLogger(__name__)


class EmailListView(generics.ListCreateAPIView):
	queryset = Email.objects.all()
	serializer_class = EmailSerializer
	filterset_fields = ['subject', 'email_from', 'email_date', 'category']

class EmailDetailView(generics.RetrieveAPIView):
	queryset = Email.objects.all()
	serializer_class = EmailSerializer
	pagination_class = None

class EmailSenderListView(generics.ListAPIView):
	queryset = Email.objects.values('email_from').distinct()
	serializer_class = EmailSerializer