from django.urls import path, re_path
from . import views


urlpatterns = [
	path("email/", views.EmailListView.as_view()),
	path("email/sender/", views.EmailSenderListView.as_view())
]