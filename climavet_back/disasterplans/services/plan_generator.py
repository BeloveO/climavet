from typing import Dict, Any, List
from disasterplans.models import DisasterPlan, DisasterType
from ..data.disaster_protocols import DISASTER_PROTOCOLS
from clinics.models import Clinic

class DisasterPlanGenerator:
    """Service class responsible for generating disaster plans based on risk assessments and predefined protocols."""

    @staticmethod
    def generate_plan(clinic: Clinic, disaster_type: DisasterType, risk_assessment_data: Dict[str, Any]) -> DisasterPlan:
        """
        Generate a disaster plan for a given clinic and disaster type based on risk assessment data.

        :param clinic: The clinic for which the disaster plan is being generated.
        :param disaster_type: The type of disaster for which the plan is being generated.
        :param risk_assessment_data: The data from the risk assessment that will inform the plan generation.
        :return: A DisasterPlan instance with the generated plan details.
        """
        # Fetch the protocol for the specified disaster type
        protocol = DISASTER_PROTOCOLS.get(disaster_type.category)
        
        if not protocol:
            raise ValueError(f"No protocol found for disaster type: {disaster_type.category}")
        
        # Here you can add logic to customize the protocol based on the risk assessment data
        # For example, you might want to adjust preparation steps based on specific vulnerabilities identified in the assessment
        
        # Create and return the DisasterPlan instance
        disaster_plan = DisasterPlan.objects.create(
            clinic=clinic,
            name=f"{disaster_type.category} Preparedness Plan",
            description=f"A comprehensive preparedness plan for {disaster_type.name.lower()}s.",
            disaster_type=disaster_type.category,
            preparation_steps=protocol['preparation_steps'],
            response_steps=protocol['response_steps'],
            recovery_steps=protocol['recovery_steps'],
            emergency_contacts=protocol['emergency_contacts'],
            supplies_needed=protocol['supplies_needed'],
            training_requirements=protocol['training_requirements']
        )
        
        return disaster_plan