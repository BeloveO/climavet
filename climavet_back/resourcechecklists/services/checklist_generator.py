from typing import List, Dict
from disasterplans.models import DisasterType, DisasterPlan
from clinics.models import Clinic
from ..models import ResourceChecklist, ResourceChecklistItem, ChecklistTemplate, ClinicResourceChecklist
from ..data.resource_database import RESOURCE_DATABASE


class ChecklistGenerator:
    """Service class responsible for generating resource checklists based on disaster plans and predefined resource data."""