from rest_framework import serializers
from email_scrape.models import Email


class EmailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Email
		fields = ('subject', 'email_from', 'email_date', 'email_body_text', 'email_body_html')