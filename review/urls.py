from django.urls import include, path, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt


router = DefaultRouter()
router.register(r'review', views.ReviewViewSet)
# router.register(r'scrape-status', views.ScrapeReviewStatusViewSet)

urlpatterns = [
	path('score/all/', views.api_restaurant_scores_view),
	path('score/', views.api_scores_detail_view),
	path('score/period/', views.scores_period_view),
	path('', include(router.urls)),
	path('import_review/', csrf_exempt(views.import_review_view)),
]