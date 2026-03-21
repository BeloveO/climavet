from .models import (DisasterPlan, DisasterType, DisasterScenario,
                     ClinicTypes, SpeciesTypes, ServiceTypes)
from rest_framework import serializers


class DisasterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterType
        fields = '__all__'

class DisasterScenarioSerializer(serializers.ModelSerializer):
    disaster_type = DisasterTypeSerializer(read_only=True)
    
    class Meta:
        model = DisasterScenario
        fields = [
            'id', 'disaster_type', 'likelihood', 'severity',
            'preparation_steps', 'immediate_actions', 'during_disaster',
            'recovery_steps', 'critical_supplies', 'evacuation_protocols',
            'equipment_protection', 'communication_plan'
        ]

class DisasterPlanSerializer(serializers.ModelSerializer):
    scenarios = DisasterScenarioSerializer(many=True, read_only=True)
    clinic_type_name = serializers.CharField(source='clinic_type.name', read_only=True)
    
    class Meta:
        model = DisasterPlan
        fields = [
            'id', 'clinic', 'created_at', 'updated_at',
            'clinic_type', 'clinic_type_name', 'service_types', 'species_treated',
            'location', 'province', 'is_flood_zone', 'is_wildfire_zone',
            'is_earthquake_zone', 'risk_score', 'is_completed', 'scenarios'
        ]
        read_only_fields = ['created_at', 'updated_at', 'risk_score', 'is_completed']

class DisasterPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterPlan
        fields = '__all__'

class ClinicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicTypes
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTypes
        fields = '__all__'


class SpeciesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeciesTypes
        fields = '__all__'