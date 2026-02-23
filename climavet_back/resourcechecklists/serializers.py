from .models import ResourceChecklist, ResourceChecklistItem, ChecklistTemplate, ClinicResourceChecklist
from rest_framework import serializers

class ResourceChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceChecklistItem
        fields = '__all__'

class ResourceChecklistSerializer(serializers.ModelSerializer):
    items = ResourceChecklistItemSerializer(many=True, read_only=True)
    class Meta:
        model = ResourceChecklist
        fields = '__all__'

class ChecklistTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistTemplate
        fields = '__all__'

class ClinicResourceChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicResourceChecklist
        fields = '__all__'