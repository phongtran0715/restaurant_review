import time
import environ
import email.utils
from email_scrape.outlook import Outlook
from email_scrape.models import Email


env = environ.Env(
	DEBUG=(bool, False)
)
environ.Env.read_env()

def fetch_inbox_mail():
	mail = Outlook()
	mail.login(env('FETCH_EMAIL'),env('FETCH_EMAIL_PASSWORD'))
	mail.select('Inbox')
	all_ids = mail.allIds(startDate)
	# all_ids = mail.unreadIds(startDate)

	if len(all_ids) == 1 and all_ids[0] == '':
		print("Not found any new email")
		return

	print("Number of email : %d" % len(all_ids))

	for item in all_ids:
		if item is None or item == '':
			continue
		try:
			mail.getEmail(item)
			mail_date = mail.maildate()
			mail_date= email.utils.parsedate(date)
			mail_date= time.strftime('%Y-%m-%d', date[:9])
			email_item = Email.objects.create(email_id=item, subject=mail.mailsubject(),
				email_from=mail.mailfrom(), email_body=mail.get_decoded_email_html_body(),
				email_date=mail_date)
			email_item.save()
		except Exception as e:
			print("Error when process email : " + item)
			print(e)
		time.sleep(1)

