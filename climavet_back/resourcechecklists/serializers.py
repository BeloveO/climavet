from .models import ResourceChecklist, ResourceChecklistItem, ChecklistTemplate, ClinicResourceChecklist
from rest_framework import serializers

class ResourceChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceChecklistItem
        fields = '__all__'

class ResourceChecklistSerializer(serializers.ModelSerializer):
    items = ResourceChecklistItemSerializer(many=True, read_only=True)
    disaster_plan_name = serializers.CharField(source='disaster_plan.name', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    total_items = serializers.IntegerField(source='items.count', read_only=True)
    items_in_stock = serializers.IntegerField(source='items.filter(status="IN_STOCK").count', read_only=True)
    completion_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    items_by_category = serializers.SerializerMethodField()
    items_by_priority = serializers.SerializerMethodField()
    items_out_of_stock = serializers.SerializerMethodField()
    class Meta:
        model = ResourceChecklist
        fields = '__all__'
    
    def get_items_by_category(self, obj):
        items = obj.items.all()
        categories = {}
        for item in items:
            category = item.category
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def get_items_by_priority(self, obj):
        items = obj.items.all()
        priorities = {}
        for item in items:
            priority = item.priority
            priorities[priority] = priorities.get(priority, 0) + 1
        return priorities
    
    def get_items_in_stock(self, obj):
        return obj.items.filter(status="IN_STOCK").count()

    def get_items_out_of_stock(self, obj):
        return obj.items.filter(status="OUT_OF_STOCK").count()

class ChecklistTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistTemplate
        fields = '__all__'

class ClinicResourceChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicResourceChecklist
        fields = '__all__'