from typing import Dict, Any, List
from disasterplans.models import DisasterPlan, DisasterType, DisasterScenario, SpeciesTypes
from ..data.disaster_protocols import DISASTER_PROTOCOLS

class IntelligentDisasterPlanGenerator:
    """
    Service class to generate disaster plans based on predefined protocols and clinic-specific data.
    This class can be extended in the future to incorporate AI-generated content or more complex logic, but for now it serves as a structured way to create plans based on existing protocols.
    """
    def __init__(self, plan: DisasterPlan):
        self.plan = plan
        self.clinic_type = plan.clinic_type
        self.service_types = list(plan.service_types.all())
        self.species_types = list(plan.species_types.all())
        self.location = {
            'city': plan.city,
            'province': plan.province,
            'is_flood_zone': plan.is_flood_zone,
            'is_wildfire_zone': plan.is_wildfire_zone,
            'is_earthquake_zone': plan.is_earthquake_zone,
        }

    def generate(self) -> DisasterPlan:
        """
        Main method to generate the customized disaster plan. It will populate the plan's description, vulnerabilities, and scenarios based on the selected disaster type and clinic characteristics.
        """
        # Step 1: Identify applicable disaster
        disasters = self._identify_applicable_disasters()

        # Step 2: Assess vulnerabilities
        vulnerability_analysis = self._assess_vulnerabilities(disasters)

        # Step 3: Generate customized scenarios
        for disaster, analysis in vulnerability_analysis.items():
            self._create_customized_scenario(disaster, analysis)

        # Step 4: Calculate overall risk score (simple average of scenario risks for now)
        self.plan.risk_score = self._calculate_risk_score(vulnerability_analysis)
        self.plan.vulnerabilities = self._format_vulnerabilities(vulnerability_analysis)
        self.plan.is_completed = True
        self.plan.save()
        
        return self.plan
    
    def _identify_disasters(self) -> List[DisasterType]:
        """
        Identify which disasters are relevant to the clinic based on location and clinic type.
        """
        disasters = []

        # Location-based disasters
        if self.location['is_flood_zone']:
            disasters.append(DisasterType.objects.get(name='Flood'))
        if self.location['is_wildfire_zone']:
            disasters.append(DisasterType.objects.get(name='Wildfire'))
        if self.location['is_earthquake_zone']:
            disasters.append(DisasterType.objects.get(name='Earthquake'))

        # Province-specific disasters 
        province_disasters = {
            'AB': ['COLD_WAVE', 'BLIZZARD', 'TORNADO', 'HEATWAVE'],
            'BC': ['WILDFIRE', 'EARTHQUAKE', 'FLOOD'],
            'ON': ['TORNADO', 'HEATWAVE', 'FLOOD', 'COLD_WAVE'],
            'QC': ['COLD_WAVE', 'FLOOD', 'BLIZZARD'],
            'MB': ['FLOOD', 'COLD_WAVE', 'BLIZZARD'],
            'SK': ['TORNADO', 'COLD_WAVE', 'BLIZZARD'],
            'NB': ['HURRICANE', 'COLD_WAVE', 'FLOOD'],
            'NS': ['HURRICANE', 'BLIZZARD', 'FLOOD'],
            'PE': ['HURRICANE', 'BLIZZARD'],
            'NL': ['HURRICANE', 'BLIZZARD', 'COLD_WAVE'],
        }
        province_disasters_list = province_disasters.get(self.location['province'], [])
        for disaster_category in province_disasters_list:
            try:
                disaster_type = DisasterType.objects.get(category=disaster_category)
                if disaster_type not in disasters:
                    disasters.append(disaster_type)
            except DisasterType.DoesNotExist:
                continue

        # Clinic type may increase certain disaster risks
        if self.clinic_type.code == 'MOBILE':
            # Mobile clinics more vulnerable to wind-based disasters
            for category in ['TORNADO', 'HURRICANE']:
                try:
                    disaster = DisasterType.objects.get(category=category)
                    if disaster not in disasters:
                        disasters.append(disaster)
                except DisasterType.DoesNotExist:
                    pass

        return disasters
    
    def _analyze_vulnerabilities(self, disasters: List[DisasterType]) -> Dict:
        """Deep analysis of vulnerabilities for each disaster"""
        analysis = {}
        
        for disaster in disasters:
            vulnerability = {
                'likelihood': self._calculate_likelihood(disaster),
                'severity': self._calculate_severity(disaster),
                'reasons': self._identify_vulnerability_reasons(disaster),
                'critical_factors': self._identify_critical_factors(disaster),
            }
            analysis[disaster] = vulnerability
        
        return analysis
    
    def _calculate_likelihood(self, disaster: DisasterType) -> str:
        """Calculate likelihood based on location and clinic type"""
        score = 0
        
        # Base score from location
        if disaster.category == 'FLOOD' and self.location['is_flood_zone']:
            score += 3
        elif disaster.category == 'WILDFIRE' and self.location['is_wildfire_zone']:
            score += 3
        elif disaster.category == 'EARTHQUAKE' and self.location['is_earthquake_zone']:
            score += 3
        else:
            score += 1  # Provincial baseline
        
        # Clinic type vulnerability
        clinic_vulnerability = self.clinic_type.vulnerability_factors.get(disaster.category, 'medium')
        if clinic_vulnerability == 'high':
            score += 1
        
        # Scoring
        if score >= 4:
            return 'high'
        elif score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_severity(self, disaster: DisasterType) -> str:
        """Calculate potential severity of impact"""
        score = 0
        
        # Service type impacts
        for service in self.service_types:
            if service.unavailability_impact == 'critical':
                score += 3
            elif service.unavailability_impact == 'high':
                score += 2
            elif service.unavailability_impact == 'medium':
                score += 1
        
        # Species considerations
        for species in self.species_types:
            if species.evacuation_priority == 1:  # Critical to evacuate
                score += 2
            elif species.evacuation_priority == 2:
                score += 1
        
        # Mobile clinics have different severity profile
        if self.clinic_type.code == 'MOBILE' and disaster.category in ['TORNADO', 'HURRICANE']:
            score += 2
        
        # Teaching hospitals and shelters have higher severity (more animals)
        if self.clinic_type.code in ['TEACHING_HOSPITAL', 'ANIMAL_SHELTER']:
            score += 1
        
        # Scoring
        if score >= 6:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'
        
    def _identify_vulnerability_reasons(self, disaster: DisasterType) -> List[str]:
        """Explain WHY this clinic is vulnerable"""
        reasons = []
        
        # Location reasons
        if disaster.category == 'FLOOD' and self.location['is_flood_zone']:
            reasons.append(f"Located in designated flood zone near {self.location['city']}")
        
        if disaster.category == 'WILDFIRE' and self.location['is_wildfire_zone']:
            reasons.append("Facility in wildfire-prone area (forest/grassland interface)")
        
        # Clinic type reasons
        if self.clinic_type.code == 'MOBILE':
            if disaster.category in ['TORNADO', 'HURRICANE']:
                reasons.append("Mobile clinic structure highly vulnerable to high winds")
        
        if self.clinic_type.code == 'ANIMAL_SHELTER':
            reasons.append("High animal population requires extensive evacuation planning")
        
        if self.clinic_type.code == 'TEACHING_HOSPITAL':
            reasons.append("Large facility with valuable equipment and multiple departments")
        
        # Service reasons
        emergency_services = [s for s in self.service_types if 'EMERGENCY' in s.code or 'CRITICAL' in s.code]
        if emergency_services:
            reasons.append("Emergency/critical care services cannot be interrupted without severe consequences")
        
        # Species reasons
        large_animals = [s for s in self.species_types if s.code in ['LARGE_ANIMAL', 'EQUINE']]
        if large_animals:
            reasons.append("Large animal evacuation requires specialized equipment and significant advance planning")
        
        exotic_species = [s for s in self.species_types if 'EXOTIC' in s.code]
        if exotic_species:
            reasons.append("Exotic species have specific environmental requirements that may be disrupted")
        
        return reasons
    
    def _identify_critical_factors(self, disaster: DisasterType) -> Dict:
        """Identify the most critical factors for this disaster"""
        factors = {
            'evacuation_complexity': 'low',
            'equipment_value': 'medium',
            'continuity_importance': 'medium',
            'staff_safety_risk': 'medium',
        }
        
        # Evacuation complexity
        if len(self.species_types) > 2:
            factors['evacuation_complexity'] = 'high'
        elif any(s.code in ['LARGE_ANIMAL', 'EQUINE', 'EXOTIC_AND_AVIAN'] for s in self.species_types):
            factors['evacuation_complexity'] = 'high'
        
        # Equipment value
        if self.clinic_type.code in ['TEACHING_HOSPITAL', 'SPECIALTY']:
            factors['equipment_value'] = 'critical'
        elif any('SPECIALTY' in s.code or 'EMERGENCY' in s.code for s in self.service_types):
            factors['equipment_value'] = 'high'
        
        # Continuity importance
        emergency_services = any('EMERGENCY' in s.code or 'CRITICAL' in s.code for s in self.service_types)
        if emergency_services:
            factors['continuity_importance'] = 'critical'
        
        # Staff safety
        if disaster.category in ['WILDFIRE', 'FLOOD', 'TORNADO', 'HURRICANE']:
            factors['staff_safety_risk'] = 'high'
        
        return factors
    
    def _create_customized_scenario(self, disaster: DisasterType, analysis: Dict):
        """Create highly customized scenario based on analysis"""
        
        # Get base protocol
        protocol = DISASTER_PROTOCOLS.get(disaster.category, {})
        
        # Customize each section
        preparation = self._customize_preparation(disaster, protocol, analysis)
        immediate = self._customize_immediate_actions(disaster, protocol, analysis)
        during = self._customize_during_actions(disaster, protocol, analysis)
        recovery = self._customize_recovery(disaster, protocol, analysis)
        supplies = self._customize_supplies(disaster, protocol, analysis)
        evacuation = self._generate_evacuation_protocols(disaster, analysis)
        equipment = self._generate_equipment_protection(disaster, analysis)
        communication = self._generate_communication_plan(disaster, analysis)
        species_actions = self._generate_species_specific_actions(disaster, analysis)
        service_actions = self._generate_service_specific_actions(disaster, analysis)
        
        # Create scenario
        DisasterScenario.objects.create(
            plan=self.plan,
            disaster_type=disaster,
            likelihood=analysis['likelihood'],
            severity=analysis['severity'],
            risk_rationale=analysis['reasons'],
            preparation_steps=preparation,
            immediate_actions=immediate,
            during_disaster=during,
            recovery_steps=recovery,
            critical_supplies=supplies,
            evacuation_protocols=evacuation,
            equipment_protection=equipment,
            communication_plan=communication,
            species_specific_actions=species_actions,
            service_specific_actions=service_actions,
        )
    
    def _customize_preparation(self, disaster: DisasterType, protocol: Dict, analysis: Dict) -> List[str]:
        """Generate customized preparation steps"""
        steps = protocol.get('preparation', []).copy()
        
        # Clinic-type specific
        if self.clinic_type.code == 'MOBILE':
            steps.insert(0, f"Identify multiple safe parking locations away from {disaster.name.lower()} risk")
            steps.append("Create vehicle-specific emergency kit with tools and supplies")
        
        if self.clinic_type.code == 'ANIMAL_SHELTER':
            steps.append(f"Develop mass evacuation plan for {disaster.name} - capacity planning for all animals")
            steps.append("Establish mutual aid agreements with other shelters in safe zones")
        
        if self.clinic_type.code == 'TEACHING_HOSPITAL':
            steps.append("Coordinate with university emergency management system")
            steps.append("Protect research equipment and data according to institutional protocols")
        
        # Service-specific
        for service in self.service_types:
            if 'EMERGENCY' in service.code:
                steps.append(f"Identify alternate {disaster.name} emergency service location within 50km")
                steps.append("Create patient transfer protocols for critical cases")
        
        # Species-specific
        for species in self.species_types:
            if species.code == 'LARGE_ANIMAL':
                steps.append(f"Arrange large animal transport for {disaster.name} evacuation (trailers, haulers)")
            elif species.code == 'EXOTIC_AND_AVIAN':
                steps.append("Stock specialized carriers and environmental control equipment")
        
        return steps
    
    def _customize_immediate_actions(self, disaster: DisasterType, protocol: Dict, analysis: Dict) -> List[str]:
        """Actions when disaster is imminent (24-48 hours)"""
        actions = protocol.get('immediate', []).copy()
        
        # Add time-critical actions based on complexity
        if analysis['critical_factors']['evacuation_complexity'] == 'high':
            actions.insert(0, f"BEGIN EVACUATION IMMEDIATELY - {disaster.name} requires extended time for complex animal transport")
        
        # Service continuity
        if analysis['critical_factors']['continuity_importance'] == 'critical':
            actions.insert(0, "Activate emergency service continuity plan - transfer critical patients to alternate facility")
        
        return actions
    
    def _customize_during_actions(self, disaster: DisasterType, protocol: Dict, analysis: Dict) -> List[str]:
        """Actions during the disaster"""
        actions = protocol.get('during', []).copy()
        
        # Always add Environment Canada monitoring
        actions.insert(0, f"Monitor Environment Canada {disaster.name} alerts and updates continuously")
        
        return actions
    
    def _customize_recovery(self, disaster: DisasterType, protocol: Dict, analysis: Dict) -> List[str]:
        """Recovery actions"""
        steps = protocol.get('recovery', []).copy()
        
        # Service-specific recovery priorities
        emergency_services = any('EMERGENCY' in s.code for s in self.service_types)
        if emergency_services:
            steps.insert(0, "Resume emergency services as top priority - even if from temporary location")
        
        return steps
    
    def _customize_supplies(self, disaster: DisasterType, protocol: Dict, analysis: Dict) -> List[Dict]:
        """Generate customized supply list"""
        supplies = []
        
        # Base disaster supplies
        for item in protocol.get('supplies', []):
            supplies.append({
                'item': item,
                'quantity': 'TBD',
                'priority': 'high',
                'category': 'general'
            })
        
        # Species-specific supplies
        for species in self.species_types:
            for supply in species.critical_supplies:
                supplies.append({
                    'item': f'{supply} for {species.name}',
                    'quantity': 'Based on animal count',
                    'priority': 'critical' if species.evacuation_priority == 1 else 'high',
                    'category': 'species-specific',
                    'species': species.name
                })
        
        # Service-specific equipment
        for service in self.service_types:
            for equipment in service.critical_equipment:
                supplies.append({
                    'item': f'Backup/protection for {equipment}',
                    'quantity': '1',
                    'priority': 'critical' if service.unavailability_impact == 'critical' else 'high',
                    'category': 'equipment',
                    'service': service.name
                })
        
        return supplies
    
    def _generate_evacuation_protocols(self, disaster: DisasterType, analysis: Dict) -> Dict:
        """Species-specific evacuation instructions"""
        protocols = {}
        
        for species in self.species_types:
            protocols[species.name] = {
                'priority': species.evacuation_priority,
                'evacuation_order': 'IMMEDIATE' if species.evacuation_priority == 1 else 'SECONDARY',
                'requirements': species.evacuation_requirements,
                'handling_notes': species.handling_notes,
                'estimated_time': self._estimate_evacuation_time(species),
                'transport_method': self._determine_transport_method(species, disaster),
            }
        
        return protocols
    
    def _estimate_evacuation_time(self, species: SpeciesTypes) -> str:
        """Estimate time needed to evacuate this species"""
        if species.code == 'LARGE_ANIMAL':
            return "4-8 hours (requires specialized transport)"
        elif species.code == 'EXOTIC_AND_AVIAN':
            return "2-4 hours (requires environmental control)"
        else:
            return "1-2 hours"
    
    def _determine_transport_method(self, species: SpeciesTypes, disaster: DisasterType) -> str:
        """Determine best transport method for species during this disaster"""
        if species.code == 'LARGE_ANIMAL':
            return "Large animal trailer with experienced hauler"
        elif species.code == 'EXOTIC_AND_AVIAN':
            return "Climate-controlled vehicle with specialized carriers"
        else:
            return "Standard vehicle with secure carriers"
    
    def _generate_equipment_protection(self, disaster: DisasterType, analysis: Dict) -> List[Dict]:
        """How to protect critical equipment"""
        protection = []
        
        # Collect all critical equipment
        all_equipment = []
        for service in self.service_types:
            all_equipment.extend(service.critical_equipment)
        
        for equipment in set(all_equipment):
            protection_steps = []
            
            if disaster.category == 'FLOOD':
                protection_steps = [
                    "Elevate to highest floor",
                    "Cover with waterproof tarp",
                    "Document serial numbers with photos"
                ]
            elif disaster.category == 'WILDFIRE':
                protection_steps = [
                    "Move to fireproof storage if available",
                    "Document with photos and serial numbers",
                    "Create off-site inventory backup"
                ]
            elif disaster.category in ['TORNADO', 'HURRICANE']:
                protection_steps = [
                    "Secure to floor or wall",
                    "Move away from windows",
                    "Disconnect from power"
                ]
            
            protection.append({
                'equipment': equipment,
                'actions': protection_steps,
                'priority': 'critical' if 'anesthesia' in equipment.lower() or 'oxygen' in equipment.lower() else 'high'
            })
        
        return protection
    
    def _generate_communication_plan(self, disaster: DisasterType, analysis: Dict) -> Dict:
        """Emergency communication protocols"""
        return {
            'staff_notification': {
                'primary_method': 'Phone tree and group text',
                'backup_method': 'Email list',
                'check_in_frequency': 'Every 6 hours during event',
                'emergency_meeting_point': 'TBD - identify safe location'
            },
            'client_communication': {
                'methods': ['Website update', 'Social media', 'Voicemail message'],
                'message_template': f'Clinic temporarily closed due to {disaster.name}. Emergency services diverted to [ALTERNATE CLINIC]. Call XXX for urgent needs.',
            },
            'emergency_contacts': [
                {'role': 'Fire Department', 'number': '911'},
                {'role': 'Non-emergency Police', 'number': '311'},
                {'role': 'Provincial Emergency Line', 'number': f'{self.location["province"]} Emergency Management'},
                {'role': 'Alternate Vet Clinic', 'number': 'TBD'},
                {'role': 'Animal Control', 'number': 'TBD'},
            ],
            'status_updates': [
                'Clinic operational status',
                'Staff safety status',
                'Animal welfare status',
                'Estimated reopening time',
            ]
        }
    
    def _generate_species_specific_actions(self, disaster: DisasterType, analysis: Dict) -> Dict:
        """Actions specific to each species type"""
        actions = {}
        
        for species in self.species_types:
            species_actions = {
                'before_disaster': [],
                'during_disaster': [],
                'after_disaster': []
            }
            
            if species.code == 'LARGE_ANIMAL':
                species_actions['before_disaster'] = [
                    f"Contact large animal haulers 48+ hours before {disaster.name}",
                    "Prepare halters and lead ropes for all animals",
                    "Identify destination (arena, fairgrounds, safe pasture)"
                ]
                species_actions['during_disaster'] = [
                    "Keep animals calm and secured",
                    "Monitor for stress and injury",
                    "Maintain communication with destination facility"
                ]
            
            elif species.code == 'EXOTIC_AND_AVIAN':
                species_actions['before_disaster'] = [
                    "Prepare climate-controlled transport",
                    "Stock heat lamps and portable heating",
                    f"Ensure backup power for environmental control during {disaster.name}"
                ]
                species_actions['during_disaster'] = [
                    "Maintain temperature control (species-specific requirements)",
                    "Minimize stress and handling",
                    "Monitor for respiratory issues"
                ]
            
            elif species.code == 'SMALL_ANIMAL':
                species_actions['before_disaster'] = [
                    "Prepare carriers for all animals",
                    "Stock 7-day food and medication supply",
                    "Update identification tags"
                ]
            
            actions[species.name] = species_actions
        
        return actions
    
    def _generate_service_specific_actions(self, disaster: DisasterType, analysis: Dict) -> Dict:
        """Actions specific to each service type"""
        actions = {}
        
        for service in self.service_types:
            service_actions = {
                'continuity_measures': [],
                'critical_equipment': service.critical_equipment,
                'backup_requirements': service.backup_requirements,
            }
            
            if 'EMERGENCY' in service.code or 'CRITICAL' in service.code:
                service_actions['continuity_measures'] = [
                    f"Activate emergency service diversion plan 24 hours before {disaster.name}",
                    "Transfer critical patients to alternate facility",
                    "Establish remote triage capability",
                    "Maintain 24/7 phone line for emergency redirects"
                ]
            
            elif 'MOBILE' in service.code:
                service_actions['continuity_measures'] = [
                    f"Suspend mobile services during {disaster.name}",
                    "Secure vehicle in safe location",
                    "Notify scheduled clients of cancellations"
                ]
            
            elif 'SHELTER' in service.code:
                service_actions['continuity_measures'] = [
                    "Activate mass evacuation protocol",
                    "Contact rescue organizations for animal placement",
                    "Suspend new intakes 48 hours before disaster"
                ]
            
            actions[service.name] = service_actions
        
        return actions
    
    def _calculate_risk_score(self, analysis: Dict) -> int:
        """Calculate overall risk score 0-100"""
        if not analysis:
            return 0
        
        severity_weights = {'low': 1, 'medium': 2, 'high': 3}
        likelihood_weights = {'low': 1, 'medium': 2, 'high': 3}
        
        total_score = 0
        for disaster, data in analysis.items():
            severity = severity_weights[data['severity']]
            likelihood = likelihood_weights[data['likelihood']]
            total_score += severity * likelihood
        
        # Normalize to 0-100
        max_possible = len(analysis) * 9  # 3 * 3
        normalized = int((total_score / max_possible) * 100) if max_possible > 0 else 0
        
        return normalized
    
    def _format_vulnerabilities(self, analysis: Dict) -> Dict:
        """Format vulnerability analysis for storage"""
        formatted = {}
        
        for disaster, data in analysis.items():
            formatted[disaster.name] = {
                'likelihood': data['likelihood'],
                'severity': data['severity'],
                'reasons': data['reasons'],
                'critical_factors': data['critical_factors'],
            }
        
        return formatted