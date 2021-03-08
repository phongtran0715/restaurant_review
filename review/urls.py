from django.urls import path, re_path
from . import views

urlpatterns = [
	path('review/', views.api_get_review_view, name='get-review'),
	path('review/new/', views.api_insert_review_view, name='create_review'),
	path('score/all/', views.api_get_all_restaurant_score, name='get-all-score'),
	path('score/', views.api_get_restaurant_score, name='get-score'),
]