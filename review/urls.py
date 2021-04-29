from django.urls import path, re_path
from . import views

urlpatterns = [
	path('review/', views.api_get_review_view, name='get-review'),
	path('review/new/', views.api_insert_review_view, name='create_review'),
	path('score/all/', views.api_get_all_restaurant_score, name='get-all-score'),
	path('score/period/', views.api_get_all_restaurant_score_period, name='get-all-score-period'),
	path('score/', views.api_get_restaurant_score, name='get-score'),
	path('scrape-status/', views.get_scrape_status_view, name='get-scrape-status'),
	path('scrape-status/new/', views.insert_scrape_status_view, name='create-scrape-status'),
]