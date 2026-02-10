from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, RiskAssessmentViewSet

router = DefaultRouter()
router.register(r'', ClinicViewSet, basename='clinic')
router.register(r'risk-assessments', RiskAssessmentViewSet, basename='riskassessment')

urlpatterns = [
    path('', include(router.urls)),
]