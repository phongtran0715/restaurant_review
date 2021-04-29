from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.31.20.217', '54.252.173.242']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'