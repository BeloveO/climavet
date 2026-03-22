# plans/management/commands/seed_disaster_data.py
from django.core.management.base import BaseCommand
from disasterplans.models import DisasterType, ClinicTypes, ServiceTypes, SpeciesTypes

class Command(BaseCommand):
    help = 'Seed initial disaster planning data'

    def handle(self, *args, **kwargs):
        # Disaster Types
        disasters = [
            {'name': 'Flood', 'category': 'water', 'description': 'Water-based flooding disaster'},
            {'name': 'Wildfire', 'category': 'fire', 'description': 'Forest or grassland fire'},
            {'name': 'Hurricane', 'category': 'wind', 'description': 'Tropical cyclone'},
            {'name': 'Tornado', 'category': 'wind', 'description': 'Violent rotating column of air'},
            {'name': 'Earthquake', 'category': 'seismic', 'description': 'Ground shaking'},
            {'name': 'Blizzard', 'category': 'winter', 'description': 'Severe snowstorm'},
            {'name': 'Extreme Cold', 'category': 'temperature', 'description': 'Dangerously low temperatures'},
            {'name': 'Extreme Heat', 'category': 'temperature', 'description': 'Dangerously high temperatures'},
        ]
        
        for d in disasters:
            DisasterType.objects.get_or_create(name=d['name'], defaults=d)
        
        # Facility Types
        facilities = [
            {'name': 'Standalone Clinic'},
            {'name': 'Multi-story Building'},
            {'name': 'Basement Facility'},
            {'name': 'Mobile Clinic'},
            {'name': 'Attached to Residence'},
        ]
        
        for f in facilities:
            ClinicTypes.objects.get_or_create(name=f['name'])
        
        # Service Types
        services = [
            {'name': 'Emergency Services'},
            {'name': 'Routine Care'},
            {'name': 'Surgery'},
            {'name': 'Boarding'},
            {'name': 'Grooming'},
            {'name': 'Dental Care'},
        ]
        
        for s in services:
            ServiceTypes.objects.get_or_create(name=s['name'])
        
        # Species Categories
        species = [
            {'name': 'Small Mammals (Cats, Dogs, Rabbits)'},
            {'name': 'Large Animals (Horses, Cattle)'},
            {'name': 'Exotic Birds'},
            {'name': 'Reptiles'},
            {'name': 'Pocket Pets (Hamsters, Guinea Pigs)'},
        ]
        
        for sp in species:
            SpeciesTypes.objects.get_or_create(name=sp['name'])
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded disaster data'))