from django.urls import include, path, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	path('scrape-status-import/', csrf_exempt(views.import_scrape_status)),
]