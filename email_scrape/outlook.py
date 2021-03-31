import email
import imaplib
import smtplib
import datetime
import email.mime.multipart
import base64
import quopri
import logging

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

SMTP_SERVER= "smtp.gmail.com"
SMTP_PORT = 587

logger = logging.getLogger(__name__)
class Outlook():
	def __init__(self):
		pass

	def login(self, username, password):
		self.username = username
		self.password = password
		login_attempts = 0
		while True:
			try:
				self.imap = imaplib.IMAP4_SSL(IMAP_SERVER,IMAP_PORT)
				r, d = self.imap.login(username, password)
				assert r == 'OK', 'login failed: %s' % str (r)
				logger.info("> Signed in as %s" % self.username, d)
				return
			except Exception as err:
				logger.error(" > Sign in error: %s" % str(err))
				login_attempts = login_attempts + 1
				if login_attempts < 3:
					continue
				assert False, 'login failed'

	def sendEmailMIME(self, recipient, subject, message):
		msg = email.mime.multipart.MIMEMultipart()
		msg['to'] = recipient
		msg['from'] = self.username
		msg['subject'] = subject
		msg.add_header('reply-to', self.username)
		# headers = "\r\n".join(["from: " + "sms@kitaklik.com","subject: " + subject,"to: " + recipient,"mime-version: 1.0","content-type: text/html"])
		# content = headers + "\r\n\r\n" + message
		try:
			self.smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
			self.smtp.ehlo()
			self.smtp.starttls()
			self.smtp.login(self.username, self.password)
			self.smtp.sendmail(msg['from'], [msg['to']], msg.as_string())
			logger.info("     email replied")
		except smtplib.SMTPException:
			logger.error("Error: unable to send email")

	def sendEmail(self, recipient, subject, message):
		headers = "\r\n".join([
			"from: " + self.username,
			"subject: " + subject,
			"to: " + recipient,
			"mime-version: 1.0",
			"content-type: text/html"
		])
		content = headers + "\r\n\r\n" + message
		attempts = 0
		while True:
			try:
				self.smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
				self.smtp.ehlo()
				self.smtp.starttls()
				self.smtp.login(self.username, self.password)
				self.smtp.sendmail(self.username, recipient, content)
				logger.info("     email sent.")
				return
			except Exception as err:
				logger.error("     Sending email failed: %s" % str(err))
				attempts = attempts + 1
				if attempts < 3:
					continue
				raise Exception("Send failed. Check the recipient email address")

	def list(self):
		# self.login()
		return self.imap.list()

	def select(self, str):
		return self.imap.select(str)

	def inbox(self):
		return self.imap.select("Inbox")

	def junk(self):
		return self.imap.select("Junk")

	def logout(self):
		return self.imap.logout()

	def since_date(self, days):
		mydate = datetime.datetime.now() - datetime.timedelta(days=days)
		return mydate.strftime("%d-%b-%Y")

	def allIdsSince(self, days):
		r, d = self.imap.search(None, '(SINCE "'+self.since_date(days)+'")', 'ALL')
		list = d[0].decode().split(' ')
		return list

	def allIdsToday(self):
		return self.allIdsSince(1)

	def readIdsSince(self, days):
		r, d = self.imap.search(None, '(SINCE "'+self.date_since(days)+'")', 'SEEN')
		list = d[0].decode().split(' ')
		return list

	def readIdsToday(self):
		return self.readIdsSince(1)

	def unreadIdsSince(self, days):
		r, d = self.imap.search(None, '(SINCE "'+self.since_date(days)+'")', 'UNSEEN')
		list = d[0].decode().split(' ')
		return list

	def unreadIdsToday(self):
		return self.unreadIdsSince(1)

	def allIds(self, startDate=None):
		if startDate != None:
			r, d = self.imap.search(None, "ALL", '(SINCE "' + startDate + '")')
		else:
			r, d = self.imap.search(None, "ALL")
		list = d[0].decode().split(' ')
		return list

	def readIds(self):
		r, d = self.imap.search(None, "SEEN")
		list = d[0].decode().split(' ')
		return list

	def unreadIds(self, startDate=None):
		if startDate != None:
			r, d = self.imap.search(None, "UNSEEN", '(SINCE "' + startDate + '")')
		else:
			r, d = self.imap.search(None, "UNSEEN")
		list = d[0].decode().split(' ')
		return list

	def hasUnread(self):
		list = self.unreadIds()
		return list != ['']

	def getIdswithWord(self, ids, word):
		stack = []
		for id in ids:
			self.getEmail(id)
			if word in self.mailbody().lower():
				stack.append(id)
		return stack

	def getEmail(self, id):
		r, d = self.imap.fetch(id, "(RFC822)")
		self.raw_email = d[0][1]
		self.email_message = email.message_from_bytes(self.raw_email)
		return self.email_message

	def unread(self):
		list = self.unreadIds()
		latest_id = list[-1]
		return self.getEmail(latest_id)

	def read(self):
		list = self.readIds()
		latest_id = list[-1]
		return self.getEmail(latest_id)

	def readToday(self):
		list = self.readIdsToday()
		latest_id = list[-1]
		return self.getEmail(latest_id)

	def unreadToday(self):
		list = self.unreadIdsToday()
		latest_id = list[-1]
		return self.getEmail(latest_id)

	def readOnly(self, folder):
		return self.imap.select(folder, readonly=True)

	def writeEnable(self, folder):
		return self.imap.select(folder, readonly=False)

	def rawRead(self):
		list = self.readIds()
		latest_id = list[-1]
		r, d = self.imap.fetch(latest_id, "(RFC822)")
		self.raw_email = d[0][1]
		return self.raw_email

	def mailbody(self):
		if self.email_message.is_multipart():
			for payload in self.email_message.get_payload():
				# if payload.is_multipart(): ...
				body = (
					payload.get_payload()
					.split(self.email_message['from'])[0]
					.split('\r\n\r\n2015')[0]
				)
				return body
		else:
			body = (
				self.email_message.get_payload()
				.split(self.email_message['from'])[0]
				.split('\r\n\r\n2015')[0]
			)
			return body

	def mailsubject(self):
		return self.email_message['Subject']

	def mailfrom(self):
		return self.email_message['from']

	def mailto(self):
		return self.email_message['to']

	def maildate(self):
		return self.email_message['date']

	def mailreturnpath(self):
		return self.email_message['Return-Path']

	def mailreplyto(self):
		return self.email_message['Reply-To']

	def mailall(self):
		return self.email_message

	def contentEncode(self):
		return str(self.email_message).split('Content-Transfer-Encoding:')[1].split()[0].strip()

	def mailbodydecoded(self):
		return base64.urlsafe_b64decode(self.mailbody())

	def mailbody_mimedecoded(self):
		return quopri.decodestring(self.mailbody())

	def get_decoded_email_html_body(self):
		msg = self.email_message
		html = ""
		if msg.is_multipart():
			for part in msg.get_payload():
				if part.get_content_type() == 'text/html':
					html=base64.urlsafe_b64decode(part.get_payload()).decode('utf-8', errors='ignore')
		else:
			html=base64.urlsafe_b64decode(msg.get_payload()).decode('utf-8', errors='ignore')
		return html
	
	def get_decoded_email_body(self):
		""" Decode email body.
		Detect character set if the header is not set.
		We try to get text/plain, but if there is not one then fallback to text/html.
		:param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
		:return: Message body as unicode string
		"""

		msg = email.message_from_bytes(self.raw_email)

		text = ""
		if msg.is_multipart():
			html = ""
			for part in msg.get_payload():
				print("%s, %s" % (part.get_content_type(), part.get_content_charset()))
				if part.get_content_charset() is None:
					# We cannot know the character set, so return decoded "something"
					text = part.get_payload(decode=True)
					continue
				charset = part.get_content_charset()
				
				if part.get_content_type() == 'text/plain':
					text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
				
				if part.get_content_type() == 'text/html':
					html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
			if text is not None:
				return text.strip()
			else:
				return html.strip()
		else:
			text = str(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
		return text.strip()
