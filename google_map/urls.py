from django.urls import path
from . import views

urlpatterns = [
	path('map/', views.api_search_google_map_view, name='get-map-info'),
]