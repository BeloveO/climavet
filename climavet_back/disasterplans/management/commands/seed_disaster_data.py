# disasterplans/management/commands/seed_disaster_data.py
from django.core.management.base import BaseCommand
from django.db import transaction

from disasterplans.models import DisasterType, ClinicTypes, ServiceTypes, SpeciesTypes


DISASTERS = [
    {'category': 'FLOOD', 'name': 'Flood',
     'description': 'Overflow of water onto land that is normally dry, from rivers, heavy rain, or coastal surges.'},
    {'category': 'WILDFIRE', 'name': 'Wildfire',
     'description': 'Uncontrolled fire burning through forest, grassland, or brush.'},
    {'category': 'HEATWAVE', 'name': 'Heatwave',
     'description': 'Prolonged period of abnormally high temperatures.'},
    {'category': 'POWER_OUTAGE', 'name': 'Power Outage',
     'description': 'Loss of electrical service that disrupts refrigeration, lighting, and equipment.'},
    {'category': 'AIR_POLLUTION', 'name': 'Air Pollution',
     'description': 'Poor air quality from smoke, smog, or industrial emissions.'},
    {'category': 'EROSION', 'name': 'Erosion',
     'description': 'Loss of soil or land from water, wind, or slope instability.'},
    {'category': 'HURRICANE', 'name': 'Hurricane',
     'description': 'Tropical cyclone with sustained high winds and heavy rain.'},
    {'category': 'TORNADO', 'name': 'Tornado',
     'description': 'Violently rotating column of air extending from a storm to the ground.'},
    {'category': 'COLD_WAVE', 'name': 'Cold Wave',
     'description': 'Prolonged period of abnormally low temperatures.'},
    {'category': 'BLIZZARD', 'name': 'Blizzard',
     'description': 'Severe snowstorm with strong winds and low visibility.'},
    {'category': 'EARTHQUAKE', 'name': 'Earthquake',
     'description': 'Sudden ground shaking caused by movement along fault lines.'},
    {'category': 'AVALANCHE', 'name': 'Avalanche',
     'description': 'Rapid flow of snow down a slope, often triggered by weather or terrain.'},
]

FACILITIES = [
    'Standalone Clinic',
    'Multi-story Building',
    'Basement Facility',
    'Mobile Clinic',
    'Attached to Residence',
]

SERVICES = [
    'Emergency Services',
    'Routine Care',
    'Surgery',
    'Boarding',
    'Grooming',
    'Dental Care',
]

SPECIES = [
    'Small Mammals (Cats, Dogs, Rabbits)',
    'Large Animals (Horses, Cattle)',
    'Exotic Birds',
    'Reptiles',
    'Pocket Pets (Hamsters, Guinea Pigs)',
]


class Command(BaseCommand):
    help = 'Seed initial disaster planning data (safe to run repeatedly)'

    @transaction.atomic
    def handle(self, *args, **options):
        # Disaster types: keyed by category, so re-running never creates duplicates
        for d in DISASTERS:
            DisasterType.objects.update_or_create(
                category=d['category'],
                defaults={'name': d['name'], 'description': d['description']},
            )

        # Other types have no fixed codes yet, so key them by name
        for name in FACILITIES:
            ClinicTypes.objects.get_or_create(name=name)

        for name in SERVICES:
            ServiceTypes.objects.get_or_create(name=name)

        for name in SPECIES:
            SpeciesTypes.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS('Successfully seeded disaster data'))