from smtplib import SMTPException
from .models import ScrapeReviewStatus
import logging
from django.conf import settings
import datetime
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.conf import settings
import requests
import json
import dateutil.parser
from pprint import pprint


logger = logging.getLogger(__name__)

def sync_scrape_status():
	logger.info('Start sync_scrape_status')
	yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%d-%m-%Y")
	get_url = settings.SCRAPE_STATUS_URL.format(yesterday, yesterday)
	response = requests.get(url=get_url).json()
	for it in response:
		try:
			logger.info(it)

			err_msg = ""
			if it['error_stacktrace'] is not None:
				err_msg = it['error_stacktrace']
			review_count=0
			if 'review_count' in it and it['review_count'] is not None:
				review_count = int(it['review_count'])
			retry_count=0
			if 'retry_count' in it and it['retry_count'] is not None:
				retry_count = int(it['retry_count'])
			platform='UNKNOW'
			if 'platform' in it and it['platform'] is not None:
				platform = it['platform']

			created_date = dateutil.parser.parse(it['created_at'])
			last_updated_at = dateutil.parser.parse(it['last_updated_at'])
			status_obj = ScrapeReviewStatus(error_msg=err_msg,
				res_id=it['restaurant_id'],
				scrape_url=it['restaurant_url'],
				retry_count=retry_count,
				review_count=review_count,
				status=it['status'],
				platform=platform,
				created_date=created_date,
				last_updated_at=last_updated_at)
			status_obj.save()
		except Exception as ex:
			print(ex)
	logger.info('Finish sync_scrape_status')

def report_scrape_status():
	logger.info('Start to create report')
	context = {}
	data = []
	today = datetime.datetime.now()
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	print(yesterday)
	platforms = ScrapeReviewStatus.objects.raw('SELECT distinct(platform), 1 as id FROM scrape_status')
	for it in platforms:
		platform = it.platform
		today_scrapes = ScrapeReviewStatus.objects.filter(last_updated_at__date=yesterday, platform = platform) 
		failed_scrape_num = today_scrapes.filter(status="FAILED").count()
		scrape_url_num = today_scrapes.values('scrape_url').distinct().count()

		data.append({
			"platform" : platform,
			"failed_count" : failed_scrape_num,
			"url_count" : scrape_url_num
		})

	context['report_date'] = today.strftime("%m/%d/%Y")
	context['data'] = data

	mail_subject = 'Scrape review status daily report.'
	message = render_to_string('scrape_status/scrape_status_report.html', {
		'data': context['data'],
	})

	# to_email = 'Feedback@restaurantreview.io'
	# to_email = 'phongtran0715@gmail.com'
	email = EmailMessage(
						mail_subject, message, to=['Feedback@restaurantreview.io', 'shoaib_573@yahoo.co.in']
			)
	try:
		email.content_subtype = 'html'
		email.send()
	except SMTPException as e:
		logger.error('There was an error sending an email:', e)

	logger.info('Finish to create report')