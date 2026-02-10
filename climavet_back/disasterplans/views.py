from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import DisasterPlan, DisasterType
from .services.plan_generator import DisasterPlanGenerator
from .serializers import DisasterPlanSerializer, DisasterTypeSerializer
from clinics.models import Clinic

# Create your views here.
class DisasterPlanViewSet(viewsets.ModelViewSet):
    queryset = DisasterPlan.objects.all()
    serializer_class = DisasterPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Create a new disaster plan based on the provided clinic, disaster type, and risk assessment data.

        :param request: The HTTP request containing the clinic ID, disaster type ID, and risk assessment data.
        :return: A response containing the created disaster plan or an error message if creation fails.
        """
        data = request.data
        clinic_id = data.get('clinic')
        disaster_type_id = data.get('disaster_type')
        risk_assessment_data = data.get('risk_assessment_data')
        try:
            clinic = Clinic.objects.get(id=clinic_id)
            disaster_type = DisasterType.objects.get(id=disaster_type_id)
        except (Clinic.DoesNotExist, DisasterType.DoesNotExist):
            return Response({'error': 'Clinic or Disaster Type not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            disaster_plan = DisasterPlanGenerator.generate_plan(clinic, disaster_type, risk_assessment_data)
            serializer = self.get_serializer(disaster_plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def dowmload_plan(self, request, pk=None):
        """
        Download the disaster plan as a PDF.

        :param request: The HTTP request.
        :param pk: The primary key of the disaster plan to download.
        :return: A response containing the PDF file.
        """
        # PDF generation logic goes here
        pass
        
class DisasterTypeViewSet(viewsets.ModelViewSet):
    queryset = DisasterType.objects.all()
    serializer_class = DisasterTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

