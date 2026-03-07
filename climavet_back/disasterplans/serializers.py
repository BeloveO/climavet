from .models import DisasterPlan, DisasterType
from rest_framework import serializers

class DisasterPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterPlan
        fields = '__all__'

class DisasterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterType
        fields = '__all__'