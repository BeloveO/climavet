RESOURCE_DATABASE = {
    'Flood': {
        'items': [
            {
                'name': 'Sandbags',
                'description': 'Used to divert water and protect the clinic from flooding.',
                'units_needed': 100,
                'unit_of_measure': 'bags',
                'category': 'Flood',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a dry, easily accessible location near entrances.'
            },
            {
                'name': 'Water Pumps',
                'description': 'Used to remove water from the clinic in the event of flooding.',
                'units_needed': 2,
                'unit_of_measure': 'units',
                'category': 'Flood',
                'priority': 'Critical',
                'is_essential': True,
                'storage_recommendations': 'Store in a secure, well-ventilated area outside the clinic and ensure they are regularly maintained and fueled.'
            }
        ]
    },
    'Wildfire': {
        'items': [
            {
                'name': 'Fire Extinguishers',
                'description': 'Used to extinguish small fires and prevent them from spreading.',
                'units_needed': 10,
                'unit_of_measure': 'units',
                'category': 'Wildfire',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in easily accessible locations throughout the clinic, especially near potential fire hazards.'
            },
            {
                'name': 'Fire-Resistant Tarps',
                'description': 'Used to cover and protect outdoor equipment and supplies from wildfire damage.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Wildfire',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a dry, easily accessible location near outdoor storage areas.'
            },
        ]
    },
    'Heatwave': {
        'items': [
            {
                'name': 'Cooling Fans',
                'description': 'Used to provide relief from extreme heat and prevent heat-related illnesses.',
                'units_needed': 20,
                'unit_of_measure': 'units',
                'category': 'Heatwave',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a cool, dry location and ensure they are   maintained and in working order before heatwave season.'
            },
            {
                'name': 'Misting Systems',
                'description': 'Used to cool outdoor areas and provide relief for animals during heatwaves.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Heatwave',
                'priority': 'Low',
                'is_essential': False,
                'storage_recommendations': 'Store in a secure location near outdoor areas and ensure they are regularly maintained and in working order before heatwave season.'
            },
        ]
    },
    'Power Outage': {
        'items': [
            {
                'name': 'Backup Generators',
                'description': 'Provide emergency power to keep essential systems running during an outage.',
                'units_needed': 2,
                'unit_of_measure': 'units',
                'category': 'Power Outage',
                'priority': 'Critical',
                'is_essential': True,
                'storage_recommendations': 'Store in a secure, well-ventilated area outside the clinic and ensure they are regularly maintained and fueled.'
            },
            {
                'name': 'Uninterruptible Power Supplies (UPS)',
                'description': 'Provide temporary power to critical equipment during a power outage.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Power Outage',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a cool, dry location near critical equipment and ensure they are regularly maintained and in working order.'
            },
        ]
    },
    'Air Pollution': {
        'items': [
            {
                'name': 'Air Purifiers',
                'description': 'Used to improve indoor air quality and protect animals from harmful pollutants.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Air Pollution',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a clean, dry location and ensure they are regularly maintained and have replacement filters on hand.'
            },
            {
                'name': 'N95 Respirators',
                'description': 'Used to protect staff from inhaling harmful pollutants during periods of poor air quality.',
                'units_needed': 20,
                'unit_of_measure': 'units',
                'category': 'Air Pollution',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a clean, dry location and ensure they are easily accessible for staff during periods of poor air quality.'
            },
        ]
    },
    'Erosion': {
        'items': [
            {
                'name': 'Erosion Control Mats',
                'description': 'Used to stabilize soil and prevent erosion around the clinic.',
                'units_needed': 50,
                'unit_of_measure': 'units',
                'category': 'Erosion',
                'priority': 'Low',  
                'is_essential': False,
                'storage_recommendations': 'Store in a dry location and ensure they are easily accessible for use during erosion control efforts.'
            },
            {
                'name': 'Drainage Pipes',
                'description': 'Used to improve drainage and prevent water accumulation that can lead to erosion.',
                'units_needed': 20,
                'unit_of_measure': 'units',
                'category': 'Erosion',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a secure location near outdoor storage areas and ensure they are easily accessible for use during drainage improvement efforts.'
            },
        ]
    },
    'Hurricane': {
        'items': [
            {
                'name': 'Storm Shutters',
                'description': 'Used to protect windows and doors from hurricane-force winds and flying debris.',
                'units_needed': 20,
                'unit_of_measure': 'units',
                'category': 'Hurricane',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a secure location near windows and doors for easy access during hurricane season.'
            },
            {
                'name': 'Hurricane Straps',
                'description': 'Used to reinforce the structure of the clinic and prevent roof damage during hurricanes.',
                'units_needed': 50,
                'unit_of_measure': 'units',
                'category': 'Hurricane',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a secure location near outdoor storage areas and ensure they are easily accessible for use during hurricane season.'
            },
        ]
    },
    'Tornado': {
        'items': [
            {
                'name': 'Tornado Shelters',
                'description': 'Designated safe areas within the clinic where animals can be protected during a tornado.',
                'units_needed': 1,
                'unit_of_measure': 'unit',
                'category': 'Tornado',
                'priority': 'Critical',
                'is_essential': True,
                'storage_recommendations': 'Ensure the shelter is clearly marked, easily accessible, and stocked with necessary supplies for animal safety during tornado events.'
            },
            {
                'name': 'Reinforced Doors',
                'description': 'Used to strengthen entrances and exits to protect against flying debris during tornadoes.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Tornado',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a secure location near entrances for easy access during tornado season.'
            },
        ]
    },
    'Cold Wave': {
        'items': [
            {
                'name': 'Heating Units',
                'description': 'Used to provide warmth and prevent hypothermia in animals during extreme cold conditions.',
                'units_needed': 10,
                'unit_of_measure': 'units',
                'category': 'Cold Wave',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a dry, easily accessible location and ensure they are regularly maintained and in working order before cold wave season.'
            },
            {
                'name': 'Insulated Blankets',
                'description': 'Used to provide additional warmth and insulation for animals during cold waves.',
                'units_needed': 50,
                'unit_of_measure': 'units',
                'category': 'Cold Wave',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a clean, dry location and ensure they are easily accessible for use during cold wave conditions.'
            },
        ]
    },
    'Blizzard': {
        'items': [
            {
                'name': 'Snow Removal Equipment',
                'description': 'Used to clear snow from entrances and pathways to maintain access to the clinic during blizzards.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Blizzard',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a secure location near entrances for easy access during blizzard conditions.'
            },
            {
                'name': 'Salt or Ice Melt',
                'description': 'Used to prevent ice buildup and improve traction on walkways during blizzards.',
                'units_needed': 100,
                'unit_of_measure': 'bags',
                'category': 'Blizzard',
                'priority': 'Low',
                'is_essential': False,
                'storage_recommendations': 'Store in a dry, easily accessible location near entrances for use during blizzard conditions.'
            },
        ]
    },
    'Earthquake': {
        'items': [
            {
                'name': 'Earthquake Kits',
                'description': 'Emergency kits containing supplies such as water, food, first aid materials, and tools to use during and after an earthquake.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Earthquake',
                'priority': 'Critical',
                'is_essential': True,
                'storage_recommendations': 'Store in easily accessible locations throughout the clinic and ensure they are regularly checked and replenished as needed.'
            },
            {
                'name': 'Structural Reinforcements',
                'description': 'Materials and equipment used to reinforce the clinic’s structure and improve its ability to withstand earthquakes.',
                'units_needed': 50,
                'unit_of_measure': 'units',
                'category': 'Earthquake',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a secure location near outdoor storage areas and ensure they are easily accessible for use during earthquake preparedness efforts.'
            },
        ]
    },
    'Avalanche': {
        'items': [
            {
                'name': 'Avalanche Beacons',
                'description': 'Used to locate individuals buried in an avalanche and facilitate rescue efforts.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Avalanche',
                'priority': 'High',
                'is_essential': True,
                'storage_recommendations': 'Store in a secure location near entrances for easy access during avalanche-prone conditions.'
            },
            {
                'name': 'Avalanche Probes',
                'description': 'Used to probe through snow to locate individuals buried in an avalanche.',
                'units_needed': 5,
                'unit_of_measure': 'units',
                'category': 'Avalanche',
                'priority': 'Medium',
                'is_essential': False,
                'storage_recommendations': 'Store in a secure location near entrances for easy access during avalanche-prone conditions.'
            },
        ]
    },
}