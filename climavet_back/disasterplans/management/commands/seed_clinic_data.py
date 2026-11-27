from django.core.management.base import BaseCommand
from disasterplans.models import DisasterType, ClinicTypes, ServiceTypes, SpeciesTypes

DisasterType.objects.update_or_create(
    category="FLOOD",
    defaults={
        "name": "Flood",
        "description": "...",
        "common_regions": ["Alberta", "British Columbia"],
    },
)