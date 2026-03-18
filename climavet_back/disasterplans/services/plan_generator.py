from typing import Dict, Any, List
from disasterplans.models import DisasterPlan, DisasterType, DisasterScenario
from ..data.disaster_protocols import DISASTER_PROTOCOLS
from clinics.models import Clinic

class DisasterPlanGenerator:
    """Service class responsible for generating disaster plans based on risk assessments and predefined protocols."""

    def __init__(self, clinic: Clinic, disaster_type: DisasterType, risk_assessment_data: Dict[str, Any]):
        self.clinic = clinic
        self.disaster_type = disaster_type
        self.risk_assessment_data = risk_assessment_data

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
    
    def identify_disasters(self) -> List[DisasterType]:
        """Identify relevant disasters based on location and facility"""
        disasters = []

        # check location-based risks        
        location = self.clinic.city
        for disaster in DisasterType.objects.all():
            if location in disaster.common_regions:
                disasters.append(disaster)
        return disasters
    
    def _assess_risks(self, disasters: List[DisasterType]) -> Dict:
        """Assess likelihood and severity for each disaster"""
        assessments = {}
        
        for disaster in disasters:
            # Get base risk from disaster protocols
            protocol = DISASTER_PROTOCOLS.get(disaster.name, {})
            
            # Adjust based on facility type
            facility_vulnerability = self.facility_type.vulnerability_factors.get(
                disaster.name.lower(), 'medium'
            )
            
            # Calculate likelihood
            likelihood = self._calculate_likelihood(disaster, facility_vulnerability)
            
            # Calculate severity based on services and species
            severity = self._calculate_severity(disaster)
            
            assessments[disaster] = {
                'likelihood': likelihood,
                'severity': severity,
                'protocol': protocol
            }
        
        return assessments
    
    def _calculate_likelihood(self, disaster: DisasterType, vulnerability: str) -> str:
        """Determine likelihood of disaster affecting this clinic"""
        # This would use historical data, location, etc.
        # Simplified for example
        
        vulnerability_score = {'low': 1, 'medium': 2, 'high': 3}[vulnerability]
        
        if vulnerability_score >= 3:
            return 'high'
        elif vulnerability_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_severity(self, disaster: DisasterType) -> str:
        """Determine potential severity of impact"""
        severity_score = 0
        
        # Higher severity if emergency services are offered
        emergency_services = [s for s in self.service_types if 'emergency' in s.name.lower()]
        if emergency_services:
            severity_score += 2
        
        # Higher severity if treating large animals (harder to evacuate)
        large_animals = [s for s in self.species_treated if 'large' in s.name.lower()]
        if large_animals:
            severity_score += 2
        
        # Higher severity if exotic species (special requirements)
        exotic_species = [s for s in self.species_treated if 'exotic' in s.name.lower()]
        if exotic_species:
            severity_score += 1
        
        if severity_score >= 4:
            return 'high'
        elif severity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _create_scenario(self, disaster: DisasterType, risk_data: Dict):
        """Create detailed scenario for a specific disaster"""
        protocol = risk_data['protocol']
        
        # Generate preparation steps
        preparation = self._generate_preparation_steps(disaster, protocol)
        
        # Generate immediate actions
        immediate = self._generate_immediate_actions(disaster, protocol)
        
        # Generate during-disaster actions
        during = self._generate_during_actions(disaster, protocol)
        
        # Generate recovery steps
        recovery = self._generate_recovery_steps(disaster, protocol)
        
        # Generate supply list
        supplies = self._generate_supply_list(disaster, protocol)
        
        # Generate evacuation protocols
        evacuation = self._generate_evacuation_protocols(disaster)
        
        # Generate equipment protection
        equipment = self._generate_equipment_protection(disaster)
        
        # Generate communication plan
        communication = self._generate_communication_plan(disaster)
        
        # Create scenario in database
        DisasterScenario.objects.create(
            plan=self.plan,
            disaster_type=disaster,
            likelihood=risk_data['likelihood'],
            severity=risk_data['severity'],
            preparation_steps=preparation,
            immediate_actions=immediate,
            during_disaster=during,
            recovery_steps=recovery,
            critical_supplies=supplies,
            evacuation_protocols=evacuation,
            equipment_protection=equipment,
            communication_plan=communication
        )
    
    def _generate_preparation_steps(self, disaster: DisasterType, protocol: Dict) -> List[str]:
        """Generate disaster-specific preparation steps"""
        steps = protocol.get('preparation', []).copy()
        
        # Add facility-specific steps
        if self.facility_type.name == 'Multi-story':
            if disaster.name in ['Flood', 'Hurricane']:
                steps.append('Move critical equipment and supplies to upper floors')
        
        if self.facility_type.name == 'Basement':
            if disaster.name == 'Flood':
                steps.insert(0, 'Install sump pump and backup power')
                steps.append('Elevate all equipment off floor level')
        
        # Add service-specific steps
        for service in self.service_types:
            if 'surgery' in service.name.lower():
                steps.append('Create backup plan for ongoing surgical cases')
            if 'boarding' in service.name.lower():
                steps.append('Develop evacuation plan for boarded animals')
        
        return steps
    
    def _generate_immediate_actions(self, disaster: DisasterType, protocol: Dict) -> List[str]:
        """Actions when disaster is imminent (24-48 hours out)"""
        actions = protocol.get('immediate', []).copy()
        
        # Species-specific actions
        for species in self.species_treated:
            if 'Large Animal' in species.name:
                if disaster.name in ['Wildfire', 'Flood']:
                    actions.append(f'Arrange transport for {species.name} to safe location')
            
            if 'Exotic' in species.name or 'Bird' in species.name:
                actions.append(f'Prepare specialized carriers for {species.name}')
        
        return actions
    
    def _generate_during_actions(self, disaster: DisasterType, protocol: Dict) -> List[str]:
        """Actions during the disaster event"""
        actions = protocol.get('during', []).copy()
        
        # Add monitoring steps
        actions.append('Monitor Environment Canada weather alerts continuously')
        actions.append('Maintain communication with staff via emergency contact system')
        
        return actions
    
    def _generate_recovery_steps(self, disaster: DisasterType, protocol: Dict) -> List[str]:
        """Post-disaster recovery actions"""
        steps = protocol.get('recovery', []).copy()
        
        # Service-specific recovery
        for service in self.service_types:
            if 'emergency' in service.name.lower():
                steps.insert(0, 'Resume emergency services as soon as safely possible')
        
        return steps
    
    def _generate_supply_list(self, disaster: DisasterType, protocol: Dict) -> List[Dict]:
        """Generate critical supplies needed"""
        base_supplies = protocol.get('supplies', []).copy()
        
        supplies = []
        for item in base_supplies:
            supplies.append({
                'item': item,
                'quantity': 'TBD',  # User can customize
                'priority': 'high'
            })
        
        # Add species-specific supplies
        for species in self.species_treated:
            evac_reqs = species.evacuation_requirements
            for item in evac_reqs.get('supplies', []):
                supplies.append({
                    'item': f'{item} for {species.name}',
                    'quantity': 'TBD',
                    'priority': 'medium'
                })
        
        # Add equipment-specific supplies
        for service in self.service_types:
            for equipment in service.critical_equipment:
                supplies.append({
                    'item': f'Backup/protection for {equipment}',
                    'quantity': '1',
                    'priority': 'high'
                })
        
        return supplies
    
    def _generate_evacuation_protocols(self, disaster: DisasterType) -> Dict:
        """Species-specific evacuation instructions"""
        protocols = {}
        
        for species in self.species_treated:
            protocols[species.name] = {
                'priority_order': species.evacuation_requirements.get('priority', 'medium'),
                'carrier_type': species.evacuation_requirements.get('carrier', 'Standard carrier'),
                'special_needs': species.evacuation_requirements.get('special_needs', []),
                'transport_considerations': species.evacuation_requirements.get('transport', [])
            }
        
        return protocols
    
    def _generate_equipment_protection(self, disaster: DisasterType) -> List[Dict]:
        """How to protect critical equipment"""
        protection_steps = []
        
        equipment_list = []
        for service in self.service_types:
            equipment_list.extend(service.critical_equipment)
        
        for equipment in set(equipment_list):  # Remove duplicates
            protection = {
                'equipment': equipment,
                'actions': []
            }
            
            if disaster.name == 'Flood':
                protection['actions'].append('Elevate to highest point')
                protection['actions'].append('Cover with waterproof tarp')
            elif disaster.name == 'Wildfire':
                protection['actions'].append('Move to fireproof storage if possible')
                protection['actions'].append('Document serial numbers and photos')
            elif disaster.name in ['Hurricane', 'Tornado']:
                protection['actions'].append('Secure to prevent movement')
                protection['actions'].append('Move away from windows')
            
            protection_steps.append(protection)
        
        return protection_steps
    
    def _generate_communication_plan(self, disaster: DisasterType) -> Dict:
        """Emergency communication protocols"""
        return {
            'staff_notification': {
                'method': 'Phone tree and group text',
                'backup': 'Email list',
                'check_in_frequency': 'Every 6 hours during event'
            },
            'client_communication': {
                'method': 'Website update, social media, voicemail',
                'message': f'Clinic closed due to {disaster.name}. Emergency services diverted to [ALTERNATE CLINIC]'
            },
            'emergency_contacts': [
                {'role': 'Fire Department', 'number': '911'},
                {'role': 'Non-emergency Police', 'number': '311'},
                {'role': 'Provincial Emergency', 'number': 'TBD'},
                {'role': 'Alternate Vet Clinic', 'number': 'TBD'},
                {'role': 'Equipment Supplier', 'number': 'TBD'}
            ],
            'updates_to_provide': [
                'Clinic status (open/closed)',
                'Staff safety',
                'Animal welfare',
                'Estimated reopening time'
            ]
        }
    
    def _calculate_overall_risk(self, assessments: Dict) -> int:
        """Calculate overall risk score 0-100"""
        if not assessments:
            return 0
        
        severity_weights = {'low': 1, 'medium': 2, 'high': 3}
        likelihood_weights = {'low': 1, 'medium': 2, 'high': 3}
        
        total_score = 0
        for disaster, data in assessments.items():
            severity = severity_weights[data['severity']]
            likelihood = likelihood_weights[data['likelihood']]
            total_score += severity * likelihood
        
        # Normalize to 0-100
        max_possible = len(assessments) * 9  # 3 * 3
        normalized = int((total_score / max_possible) * 100) if max_possible > 0 else 0
        
        return normalized