from .models import DisasterPlan, DisasterType, DisasterScenario
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
    clinic_type = serializers.CharField(source='clinic.clinic_type', read_only=True)
    service_types = serializers.SerializerMethodField()
    species_treated = serializers.SerializerMethodField()
    location = serializers.CharField(source='clinic.location', read_only=True)
    province = serializers.CharField(source='clinic.province', read_only=True)
    is_flood_zone = serializers.BooleanField(source='clinic.is_flood_zone', read_only=True)
    is_wildfire_zone = serializers.BooleanField(source='clinic.is_wildfire_zone', read_only=True)
    is_earthquake_zone = serializers.BooleanField(source='clinic.is_earthquake_zone', read_only=True)

    def get_species_treated(self, obj):
        return obj.clinic.species_treated
    
    def get_service_types(self, obj):
        return obj.clinic.service_types
    
    class Meta:
        model = DisasterPlan
        fields = [
            'id', 'clinic', 'created_at', 'updated_at',
            'clinic_type', 'service_types', 'species_treated',
            'location', 'province', 'is_flood_zone', 'is_wildfire_zone',
            'is_earthquake_zone', 'risk_score', 'is_completed', 'scenarios'
        ]
        read_only_fields = ['created_at', 'updated_at', 'risk_score', 'is_completed']
