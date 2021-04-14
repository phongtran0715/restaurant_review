"""
Django settings for restaurant_review project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os, sys
from pathlib import Path
import environ

env = environ.Env(
	# set casting, default value
	DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.31.20.217', '54.252.173.242']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'review',
	'restaurant',
	'rest_framework_swagger',
	'django_crontab',
	'email_scrape',
	'google_map',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant_review.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'restaurant_review.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	'default': env.db(),
	'OPTIONS': {
			'charset': 'utf8mb4'
		}
}


REST_FRAMEWORK = {
	"DATE_INPUT_FORMATS": ["%Y-%m-%d"],
	'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'root': {
		'level': 'INFO',
		'handlers': ['file'],
	},
	'formatters': {
		'default': {
			'format': '%(levelname)s %(asctime)s %(message)s'
		}
	},
	'handlers': {
		'file': {
			'level': 'INFO',
			'class': 'logging.FileHandler',
			'formatter': 'default',
			'filename': os.path.join(BASE_DIR, 'log/general.log')
		},
		'console':{
			'level':'INFO',
			'class':'logging.StreamHandler',
			'formatter': 'default'
		},
	},
	'loggers': {
		'django': {
			'level': 'INFO',
			'handlers': ['console'],
			'propagate': True,
		}
	}
}

CRONJOBS = [
	('0 0 * * *', 'review.cron.build_restaurant_resource', 
		' >> {} 2>&1'.format(os.path.join(BASE_DIR, 'log/restaurant_calculation_job.log'))),
	('0 0 * * *', 'email_scrape.cron.fetch_inbox_mail', 
		'>> {} 2>&1'.format(os.path.join(BASE_DIR, 'log/email_scrape_job.log'))),
]
CRONTAB_LOCK_JOBS = True

DATE_INPUT_FORMATS = ['%Y-%m-%d']

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')

# User settings
FETCH_EMAIL = env('FETCH_EMAIL')
FETCH_EMAIL_PASSWORD = env('FETCH_EMAIL_PASSWORD')

PROXY_API_KEY = env('PROXY_API_KEY')


EXTERNAL_BASE = os.path.join(BASE_DIR, "externals")
EXTERNAL_LIBS_PATH = os.path.join(EXTERNAL_BASE, "libs")
EXTERNAL_APPS_PATH = os.path.join(EXTERNAL_BASE, "apps")
sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path