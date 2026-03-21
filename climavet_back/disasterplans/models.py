from django.db import models
from clinics.models import Clinic
from django.contrib.auth.models import User

# Create your models here.

class ClinicTypes(models.Model):
    """Types of veterinary facilities"""
    name = models.CharField(max_length=100)
    vulnerability_factors = models.JSONField(default=dict)
    
    def __str__(self):
        return self.name

class ServiceTypes(models.Model):
    """Veterinary services offered"""
    name = models.CharField(max_length=100)
    critical_equipment = models.JSONField(default=list)
    
    def __str__(self):
        return self.name

class SpeciesTypes(models.Model):
    """Species treated at clinic"""
    name = models.CharField(max_length=100)
    evacuation_requirements = models.JSONField(default=dict)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Species categories"

class DisasterType(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,
                                choices=[
                                    ("FLOOD", "Flood"),
                                    ("WILDFIRE", "Wildfire"),
                                    ("HEATWAVE", "Heatwave"),
                                    ("POWER_OUTAGE", "Power Outage"),
                                    ("AIR_POLLUTION", "Air Pollution"),
                                    ("EROSION", "Erosion"),
                                    ("HURRICANE", "Hurricane"),
                                    ("TORNADO", "Tornado"),
                                    ("COLD_WAVE", "Cold Wave"),
                                    ("BLIZZARD", "Blizzard"),
                                    ("EARTHQUAKE", "Earthquake"),
                                    ("AVALANCHE", "Avalanche"),
                                ])
    description = models.TextField(blank=True, null=True)
    common_regions = models.JSONField(default=list)  # List of regions commonly affected by this disaster type

    def __str__(self):
        return self.name

class DisasterPlan(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='disaster_plans')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # Clinic characteristics
    clinic_type = models.ForeignKey(ClinicTypes, on_delete=models.SET_NULL, null=True)
    service_types = models.ManyToManyField(ServiceTypes, blank=True)
    species_types = models.ManyToManyField(SpeciesTypes, blank=True)
    
    # Location details
    location = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=50, blank=True)
    is_flood_zone = models.BooleanField(default=False)
    is_wildfire_zone = models.BooleanField(default=False)
    is_earthquake_zone = models.BooleanField(default=False)

    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE)
    risk_score = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    common_regions = models.JSONField(default=list)  # List of regions commonly affected by this disaster type

    def __str__(self):
        return f"Disaster Plan for {self.clinic.name}"
    
    
class DisasterScenario(models.Model):
    """Model to represent a specific disaster scenario, which can be used for training and simulation purposes."""
    plan = models.ForeignKey(DisasterPlan, on_delete=models.CASCADE, related_name='scenarios')
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE)
    
    # Risk assessment
    likelihood = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    )
    severity = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    )
    
    # Generated action plans
    preparation_steps = models.JSONField(default=list)
    # ["Create evacuation plan", "Stock emergency supplies", ...]
    
    immediate_actions = models.JSONField(default=list)
    # Actions to take when disaster is imminent
    
    during_disaster = models.JSONField(default=list)
    # Actions during the event

    response_steps = models.JSONField(default=list)    
    
    recovery_steps = models.JSONField(default=list)
    # Post-disaster recovery
    
    critical_supplies = models.JSONField(default=list)
    # Supplies needed for this disaster
    
    evacuation_protocols = models.JSONField(default=dict)
    # Species-specific evacuation instructions
    
    equipment_protection = models.JSONField(default=list)
    # How to protect critical equipment
    
    communication_plan = models.JSONField(default=dict)
    # Emergency contacts, staff notification

    emergency_contacts = models.JSONField(default=list) # List of emergency contacts
    supplies_needed = models.JSONField(default=list)    # List of supplies needed
    training_requirements = models.JSONField(default=list) # List of training requirements

    
    class Meta:
        unique_together = ['plan', 'disaster_type']
    
    def __str__(self):
        return f"{self.disaster_type.name} - {self.plan}"
