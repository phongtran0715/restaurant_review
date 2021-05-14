from smtplib import SMTPException
from .models import ScrapeReviewStatus
import logging
from django.conf import settings
import datetime


logger = logging.getLogger(__name__)

def report_scrape_status():
	logger.info('Start to create report')
	context = {}
	data = []
	today = datetime.datetime.now()
	platforms = ScrapeReviewStatus.objects.values('platform').distinct()
	logger.info(platforms.count())
	for i in range (0, platforms.count()):
		platform = platforms[i]['platform']
		logger.info(platform)
		today_scrapes = ScrapeReviewStatus.objects.filter(last_updated_at__year=today.year, 
			last_updated_at__month=today.month, last_updated_at__day=today.day, platform = platform) 
		failed_scrape_num = today_scrapes.filter(status="FAILED").count()
		scrape_url_num = today_scrapes.values('scrape_url').distinct().count()

		data.append({
			"platform" : platform,
			"failed_count" : failed_scrape_num,
			"url_count" : scrape_url_num
		})

	context['report_date'] = today.strftime("%m/%d/%Y")
	context['data'] = data

	logger.info('context : {}'.format(context))
	logger.info('Finish to create report')