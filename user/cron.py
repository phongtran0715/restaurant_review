import logging
from .models import User
from restaurant.models import WebsitePerformance
import json
import os, time
from datetime import datetime


logger = logging.getLogger(__name__)

def get_lighthouse_report():
	logger.info("get_lighthouse_report >>>> start")
	users = User.objects.using('productiondb').all()
	for user in users:
		try:
			print(user.company_website)
			url = user.company_website
			output_file="result_{}_{}.json".format(user.id, datetime.now().strftime("%m-%d-%y"))
			command = 'lighthouse --quiet --no-update-notifier --no-enable-error-reporting --output=json --output-path={} --chrome-flags="--headless" {}'.format(output_file, url)
			stream = os.popen(command)
			# sleep 2 minutes
			time.sleep(60)
			with open(output_file) as json_data:
				loaded_json = json.load(json_data)

				performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
				accessibility = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
				best_practices = str(round(loaded_json["categories"]["best-practices"]["score"] * 100))
				seo = str(round(loaded_json["categories"]["seo"]["score"] * 100))
				first_contentful_paint = str(round(loaded_json["audits"]["first-contentful-paint"]["numericValue"]/1000, 1))
				speed_index = str(round(loaded_json["audits"]["speed-index"]["numericValue"]/1000, 1))
				interactive = str(round(loaded_json["audits"]["interactive"]["numericValue"]/1000, 1))
				largest_contentful_paint = str(round(loaded_json["audits"]["largest-contentful-paint"]["numericValue"]/1000, 1))
				total_blocking_time = str(round(loaded_json["audits"]["total-blocking-time"]["numericValue"]))
				cumulative_layout_shift = str(round(loaded_json["audits"]["cumulative-layout-shift"]["numericValue"], 3))
				
				# insert to database
				WebsitePerformance.objects.update_or_create(
					user_id=user.id,
					defaults={
						'user_id': user.id,
						'company_website': url, 
						'performance' : performance,
						'accessibility' : accessibility,
						'best_practices': best_practices,
						'seo' : seo,
						'first_contentful_paint' : first_contentful_paint,
						'speed_index': speed_index,
						'interactive' : interactive,
						'largest_contentful_paint' : largest_contentful_paint,
						'total_blocking_time' : total_blocking_time,
						'cumulative_layout_shift' : cumulative_layout_shift,
						'last_updated_at': datetime.now()
					}
				)

			# TODO: remove json file
		except Exception as ex:
			logger.error(ex)
	logger.info("get_lighthouse_report <<<< finish")