from django.db import models
from django.contrib.auth.models import AbstractUser


SUBSCRIPTIONS = [
	('free','Free'),
	('t1','Tier1'),
	('t2','Tier2'),
	('t3','Tier3'),
]
ONBOARDING = [
	('yes','Yes'),
	('no','No'),
	('inprogress','In Progress')
]


class User(AbstractUser):
	company_name = models.CharField(max_length=255, default='', blank=True,
									null=True)
	company_logo = models.ImageField(blank=True, null=True)
	company_description = models.TextField(default='', blank=True, null=True)
	company_email = models.EmailField(('company email'), blank=True, null=True)
	company_website = models.URLField(('company website'), blank=True,
									  null=True)
	email_notification = models.BooleanField("Email notification is on/off",
											 default=False)
	subscription_level = models.CharField(choices=SUBSCRIPTIONS, blank=True,null=True,max_length=250)
	onboarding = models.CharField(choices=ONBOARDING,blank=True,null=True,max_length=250)
	subscription_payment_status = models.BooleanField(default=False,blank=True,null=True)
	#Stripe details
	stripe_customer_id = models.CharField(default="", max_length=250, blank=True)
	stripe_subscription_id = models.CharField(default="",max_length=250,blank=True)
	stripe_price_id = models.CharField(default="",max_length=250,blank=True)

	class Meta:
		db_table = "reviews_user"