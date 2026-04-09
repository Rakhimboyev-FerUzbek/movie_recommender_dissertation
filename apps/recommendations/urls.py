from django.urls import path

from apps.recommendations.views import auto_recommendation_view, recommendation_lab_view

urlpatterns = [
    path("for-you/", auto_recommendation_view, name="recommend_for_you"),
    path("lab/", recommendation_lab_view, name="recommendation_lab"),
]