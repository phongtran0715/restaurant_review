from smtplib import SMTPException
from .models import ScrapeReviewStatus
import logging
from django.conf import settings
import datetime
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)

def report_scrape_status():
	logger.info('Start to create report')
	context = {}
	data = []
	today = datetime.datetime.now()
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	print(yesterday)
	platforms = ScrapeReviewStatus.objects.values('platform').distinct()
	logger.info(platforms.count())
	for i in range (0, platforms.count()):
		platform = platforms[i]['platform']
		logger.info(platform)
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

	to_email = 'Feedback@restaurantreview.io'
	email = EmailMessage(
						mail_subject, message, to=[to_email]
			)
	try:
		email.content_subtype = 'html'
		email.send()
	except SMTPException as e:
		logger.error('There was an error sending an email:', e)

	logger.info('Finish to create report')