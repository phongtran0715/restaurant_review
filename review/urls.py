from django.urls import include, path, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt


router = DefaultRouter()
router.register(r'review', views.ReviewViewSet)
router.register(r'scrape-status', views.ScrapeReviewStatusViewSet)

urlpatterns = [
	path('score/all/', views.RestaurantScoreView.as_view()),
	path('score/<int:pk>/', views.RestaurantScoreDetailView.as_view()),
	path('score/period/', views.RestaurantScorePeriodView.as_view()),
	path('', include(router.urls)),
	path('import_scrape_review/', csrf_exempt(views.import_scrape_review_view)),
]