from django.urls import path
from . import views

urlpatterns = [
	path('map/', views.SearchGoogleMapView.as_view()),
	path('google/', views.SearchGoogleView.as_view()),
]