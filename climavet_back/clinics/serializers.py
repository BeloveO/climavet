from rest_framework import serializers
from .models import Clinic, RiskAssessment

class ClinicSerializer(serializers.ModelSerializer):
    overall_risk = serializers.SerializerMethodField()
    def get_overall_risk(self, obj):
        risk_assessment = obj.risk_assessments.order_by('-assessment_date').first()
        if risk_assessment:
            return risk_assessment.overall_score
        return None
    class Meta:
        model = Clinic
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']

class RiskAssessmentSerializer(serializers.ModelSerializer):
    overall_score = serializers.ReadOnlyField()
    class Meta:
        model = RiskAssessment
        fields = '__all__'