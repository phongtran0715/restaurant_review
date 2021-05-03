from django.urls import path, re_path
from restaurant import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'restaurant', views.RestaurantViewSet)
urlpatterns = router.urls