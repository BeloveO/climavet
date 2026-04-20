from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DisasterPlanViewSet, DisasterTypeViewSet, 
                    ClinicTypeViewSet, ServiceTypeViewSet, SpeciesTypeViewSet)

router = DefaultRouter()

router.register(r'plans', DisasterPlanViewSet, basename='disaster-plan')
router.register(r'types', DisasterTypeViewSet, basename='disaster-type')
router.register(r'clinic-types', ClinicTypeViewSet, basename='clinic-type')
router.register(r'service-types', ServiceTypeViewSet, basename='service-type')
router.register(r'species-types', SpeciesTypeViewSet, basename='species-type')

urlpatterns = [
    path('', include(router.urls)),
]