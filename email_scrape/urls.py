from django.urls import path, re_path
from . import views


urlpatterns = [
	path("email/", views.get_email_view, name="get-email")
]