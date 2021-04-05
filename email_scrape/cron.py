import time
import environ
import email.utils
from email_scrape.outlook import Outlook
from email_scrape.models import Email
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def format_mail_from(mail_from):
	if "<" in mail_from:
		mail_from = mail_from.split("<")[1]

	if ">" in mail_from:
		mail_from = mail_from.split(">")[0]

	return mail_from.strip()

def fetch_inbox_mail():
	logger.info("Start to scrape email")
	mail = Outlook()
	mail.login(settings.FETCH_EMAIL, settings.FETCH_EMAIL_PASSWORD)
	mail.select('Inbox')
	all_ids = mail.allIds()
	# all_ids = mail.unreadIds(startDate)

	if len(all_ids) == 1 and all_ids[0] == '':
		logger.warning("Not found any new email")
		return

	logger.info("Number of email : %d" % len(all_ids))

	for item in all_ids:
		if item is None or item == '':
			continue
		mail.getEmail(item)
		mail_date=email.utils.parsedate(mail.maildate())
		mail_date=time.strftime('%Y-%m-%d %H:%M:%S', mail_date)
		
		mail_from = format_mail_from(mail.mailfrom())
		text, html = mail.get_decoded_email_body()

		email_item = Email.objects.update_or_create(email_id=item,
			defaults={
				'email_id':item, 'subject':mail.mailsubject(),
				'email_from':mail_from,
				'email_body_text':text,
				'email_body_html' : html,
				'email_date':mail_date
			})
		logger.info("Id : {} - From : {} - Subject : {}\n".format(item, mail_from, mail.mailsubject()))
		time.sleep(1)
	logger.info("Finish to scrape email")

