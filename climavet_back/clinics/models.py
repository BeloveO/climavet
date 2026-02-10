from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Clinic(models.Model):
    CLINIC_TYPES = [
        ("PRIVATE", "Private"),
        ("CORPORATE", "Corporate"),
        ("MOBILE", "Mobile"),
        ("ANIMAL_SHELTER", "Animal Shelter"),
        ("TEACHING_HOSPITAL", "Teaching Hospital"),
        ("WILDLIFE_FACILITY", "Wildlife Facility"),
    ]
    SPECIES_TYPES = [
        ("SMALL_ANIMAL", "Small Animal"),
        ("EQUINE", "Equine"),
        ("FELINE", "Feline"),
        ("MIXED", "Mixed"),
        ("EXOTIC_AND_AVIAN", "Exotic and Avian"),
    ]
    SERVICE_TYPES = [
        ("GENERAL_VETERINARY_CARE", "General Veterinary Care"),
        ("EMERGENCY_OR_CRITICAL_CARE", "Emergency or Critical Care"),
        ("URGENT_CARE", "Urgent Care"),
        ("SPECIALTY_SERVICES", "Specialty Services"),
        ("MOBILE_VETERINARY_SERVICES", "Mobile Veterinary Services"),
        ("ANIMAL_SHELTER_SERVICES", "Animal Shelter Services"),
        ("TEACHING_HOSPITAL_SERVICES", "Teaching Hospital Services"),
        ("WILDLIFE_FACILITY_SERVICES", "Wildlife Facility Services"),
    ]
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    clinic_type = models.CharField(max_length=50, choices=CLINIC_TYPES)
    species_types = models.CharField(max_length=50, choices=SPECIES_TYPES)
    service_types = models.CharField(max_length=50, choices=SERVICE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class RiskAssessment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='risk_assessments')
    assessment_date = models.DateField()
    flood_risk = models.IntegerField(default=0)
    wildfire_risk = models.IntegerField(default=0)
    heatwave_risk = models.IntegerField(default=0)
    power_outage_risk = models.IntegerField(default=0)
    air_pollution_risk = models.IntegerField(default=0)
    erosion_risk = models.IntegerField(default=0)
    hurricane_risk = models.IntegerField(default=0)
    tornado_risk = models.IntegerField(default=0)
    cold_wave_risk = models.IntegerField(default=0)
    blizzard_risk = models.IntegerField(default=0)
    earthquake_risk = models.IntegerField(default=0)
    avalanche_risk = models.IntegerField(default=0)
    assessment_data = models.JSONField(default=dict)  # Store detailed assessment data as JSON  
    vulnerabilities = models.JSONField(default=list)  # Store vulnerabilities as JSON list
    recommendations = models.JSONField(default=list)  # Store recommendations as JSON list

    @property
    def overall_score(self):
        # Calculate highest risk score based on individual risks
        scores = [self.flood_risk, self.wildfire_risk, self.heatwave_risk, self.power_outage_risk, self.air_pollution_risk, self.erosion_risk]
        return max(scores) if scores else 0
        