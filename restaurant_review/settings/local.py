from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.31.20.217', '54.252.173.242']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only

INTERNAL_IPS =[
	'127.0.0.1',
	'172.31.20.217',
	'54.252.173.242'
]