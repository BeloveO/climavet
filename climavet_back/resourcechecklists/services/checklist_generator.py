from typing import List, Dict
from disasterplans.models import DisasterType, DisasterPlan
from clinics.models import Clinic
from ..models import ResourceChecklist, ResourceChecklistItem, ChecklistTemplate, ClinicResourceChecklist
from ..data.resource_database import RESOURCE_DATABASE


class ChecklistGenerator:
    """
    Generates customized resource checklists for clinics based on disaster plans and predefined resource data.
    """
    def __init__(self, clinic: Clinic, checklist: ClinicResourceChecklist, disaster_plan: DisasterPlan):
        self.clinic = clinic
        self.checklist = checklist
        self.disaster_plan = disaster_plan
    
    @staticmethod
    def generate_checklist(clinic: Clinic, disaster_plan: DisasterPlan) -> ResourceChecklist:
        """
        Generate a resource checklist for a given clinic and disaster plan.

        :param clinic: The clinic for which the checklist is being generated.
        :param disaster_plan: The disaster plan that will inform the checklist generation.
        :return: A ResourceChecklist instance with the generated checklist items.
        """
        # Fetch the base items that are essential for any disaster
        base_items = ChecklistGenerator.get_base_items()
        # Fetch additional items from the resource database based on the disaster type
        disaster_type = disaster_plan.disaster_type
        additional_items = RESOURCE_DATABASE.get(disaster_type, [])
        # Combine base items with additional items, ensuring no duplicates
        all_items = {item['name']: item for item in base_items + additional_items}.values()
        # Create a new ResourceChecklist instance
        resource_checklist = ResourceChecklist.objects.create(
            clinic=clinic,
            disaster_plan=disaster_plan,
            name=f"{disaster_plan.name} Resource Checklist",
            description=f"A checklist of resources needed for the {disaster_plan.name}."
        )
        # Create ResourceChecklistItem instances for each item in the combined list
        for item in all_items:
            ResourceChecklistItem.objects.create(
                checklist=resource_checklist,
                name=item['name'],
                description=item['description'],
                quantity_needed=item['quantity_needed'],
                unit_of_measure=item['unit_of_measure'],
                category=item['category'],
                priority=item['priority'],
                is_essential=item['is_essential']
            )
        return resource_checklist
    
    def get_base_items(self) -> List[Dict[str, str]]:
        """
        Retrieves essential items for any disaster

        :return: A list of dictionaries containing resource information.
        """
        return [
            {"name": "First Aid Kit", 
             "description": "A kit containing basic medical supplies for treating minor injuries.", 
             "quantity_needed": 1,
             "unit_of_measure": "kit",
             "category": "Medical",
             "priority": "High",
             "is_essential": True
             },
            {"name": "Emergency Contact List", 
             "description": "A list of important phone numbers and contacts for emergencies.", 
             "quantity_needed": 1,
             "unit_of_measure": "list",
             "category": "Communication",
             "priority": "High",
             "is_essential": True
             },
            {"name": "Flashlights and Batteries", 
             "description": "Portable light sources and extra batteries for use during power outages.", 
             "quantity_needed": 2,
             "unit_of_measure": "set",
             "category": "Safety",
             "priority": "Medium",
             "is_essential": True
             },
            {"name": "Water Storage Containers", 
             "description": "Containers for storing clean water in case of water supply disruption.", 
             "quantity_needed": 2,
             "unit_of_measure": "container",
             "category": "Sustenance",
             "priority": "Medium",
             "is_essential": True
            },
            {"name": "Non-Perishable Food Supplies", 
             "description": "Food items that do not require refrigeration and have a long shelf life.", 
             "quantity_needed": 3,
             "unit_of_measure": "box",
             "category": "Sustenance",
             "priority": "Medium",
             "is_essential": True
             },
            {"name": "Portable Generator", 
             "description": "A generator to provide backup power during outages.", 
             "quantity_needed": 1,
             "unit_of_measure": "unit",
             "category": "Power",
             "priority": "High",
             "is_essential": True
             },
            {"name": "Fire Extinguishers", 
             "description": "Devices for extinguishing small fires.", 
             "quantity_needed": 2,
             "unit_of_measure": "unit",
             "category": "Safety",
             "priority": "High",
             "is_essential": True
             },
        ]
    
    def create_clinic_checklist(self) -> ClinicResourceChecklist:
        """
        Create a clinic-specific resource checklist based on the generated checklist.

        :return: A ClinicResourceChecklist instance linked to the clinic and disaster plan.
        """
        return ClinicResourceChecklist.objects.create(
            clinic=self.clinic,
            disaster_plan=self.disaster_plan,
            name=f"{self.disaster_plan.name} Resource Checklist",
            description=f"A customized resource checklist for {self.clinic.name} based on the {self.disaster_plan.name}.",
            quantity_needed=0,  # This can be updated later based on inventory and needs
            unit_of_measure='unit',  # Default unit, can be updated based on specific items
            category='General',  # Default category, can be updated based on specific items
            priority='Medium',  # Default priority, can be updated based on specific items
            is_essential=False  # Default to False, can be updated based on specific items
        )