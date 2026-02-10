from django.db import models
from clinics.models import Clinic
from django.contrib.auth.models import User

# Create your models here.

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
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    preparation_steps = models.JSONField(default=list)  # List of preparation steps
    response_steps = models.JSONField(default=list)     # List of response steps
    recovery_steps = models.JSONField(default=list)     # List of recovery steps
    emergency_contacts = models.JSONField(default=list) # List of emergency contacts
    supplies_needed = models.JSONField(default=list)    # List of supplies needed
    training_requirements = models.JSONField(default=list) # List of training requirements

    
    
    