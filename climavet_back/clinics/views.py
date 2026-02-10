from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Clinic, RiskAssessment
from .serializers import ClinicSerializer, RiskAssessmentSerializer

# Create your views here.

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RiskAssessmentViewSet(viewsets.ModelViewSet):
    queryset = RiskAssessment.objects.all()
    serializer_class = RiskAssessmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Docstring for create
        
        :param self: Description
        :param request: Description
        :param args: Description
        :param kwargs: Description
        Risk assessment creation logic goes here. You can add custom validation or processing before saving the instance.
        """
        data = request.data
        clinic_id = data.get('clinic')
        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)
        # calculate overall risk score based on wizard logic (this is just a placeholder, replace with actual logic)
        scores = self.calculate_risk_scores(data)
        
        assessment = RiskAssessment.objects.create(
            clinic_id=clinic_id,
            flood_risk=scores.get('flood_risk', 0),
            wildfire_risk=scores.get('wildfire_risk', 0),
            heatwave_risk=scores.get('heatwave_risk', 0),
            power_outage_risk=scores.get('power_outage_risk', 0),
            air_pollution_risk=scores.get('air_pollution_risk', 0),
            erosion_risk=scores.get('erosion_risk', 0),
            hurricane_risk=scores.get('hurricane_risk', 0),
            tornado_risk=scores.get('tornado_risk', 0),
            cold_wave_risk=scores.get('cold_wave_risk', 0),
            blizzard_risk=scores.get('blizzard_risk', 0),
            earthquake_risk=scores.get('earthquake_risk', 0),
            avalanche_risk=scores.get('avalanche_risk', 0),
            assessment_data=data
        )
        
        # here you can also add logic to determine vulnerabilities and recommendations based on the scores
        vulnerabilities = self.identify_vulnerabilities(scores)
        assessment.vulnerabilities = vulnerabilities
        recommendations = self.generate_recommendations(scores)
        assessment.recommendations = recommendations
        assessment.save()

        serializer = self.get_serializer(assessment)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )