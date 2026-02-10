from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisasterPlanViewSet, DisasterTypeViewSet

router = DefaultRouter()

router.register(r'', DisasterPlanViewSet, basename='disasterplan')
router.register(r'disaster-types', DisasterTypeViewSet, basename='disastertype')

urlpatterns = [
    path('', include(router.urls)),
]