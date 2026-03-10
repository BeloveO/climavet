import { useState } from "react";

const ScenarioCard = ({ scenario}) => {
    const [expandedSection, setExpandedSection] = useState(null);
    
    return (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 p-6 text-white">
            <div className="flex justify-between items-start">
            <div>
                <h3 className="text-2xl font-bold">{scenario.disaster_type.name}</h3>
                <p className="mt-2 opacity-90">{scenario.disaster_type.description}</p>
            </div>
            <div className="text-right">
                <div className="text-sm opacity-90">Likelihood</div>
                <div className="text-lg font-semibold uppercase">{scenario.likelihood}</div>
                <div className="text-sm opacity-90 mt-2">Severity</div>
                <div className="text-lg font-semibold uppercase">{scenario.severity}</div>
            </div>
            </div>
        </div>
        
        {/* Sections */}
        <div className="p-6 space-y-4">
            {/* Preparation */}
            <Section
            title="📋 Preparation Steps"
            icon="🔨"
            items={scenario.preparation_steps}
            expanded={expandedSection === 'prep'}
            onToggle={() => setExpandedSection(expandedSection === 'prep' ? null : 'prep')}
            />
            
            {/* Immediate Actions */}
            <Section
            title="⚠️ Immediate Actions (24-48hr warning)"
            items={scenario.immediate_actions}
            expanded={expandedSection === 'immediate'}
            onToggle={() => setExpandedSection(expandedSection === 'immediate' ? null : 'immediate')}
            />
            
            {/* During Disaster */}
            <Section
            title="🚨 During Disaster"
            items={scenario.during_disaster}
            expanded={expandedSection === 'during'}
            onToggle={() => setExpandedSection(expandedSection === 'during' ? null : 'during')}
            />
            
            {/* Recovery */}
            <Section
            title="🔄 Recovery Steps"
            items={scenario.recovery_steps}
            expanded={expandedSection === 'recovery'}
            onToggle={() => setExpandedSection(expandedSection === 'recovery' ? null : 'recovery')}
            />
            
            {/* Critical Supplies */}
            <SuppliesSection
            supplies={scenario.critical_supplies}
            expanded={expandedSection === 'supplies'}
            onToggle={() => setExpandedSection(expandedSection === 'supplies' ? null : 'supplies')}
            />
            
            {/* Evacuation */}
            {Object.keys(scenario.evacuation_protocols).length > 0 && (
            <EvacuationSection
                protocols={scenario.evacuation_protocols}
                expanded={expandedSection === 'evacuation'}
                onToggle={() => setExpandedSection(expandedSection === 'evacuation' ? null : 'evacuation')}
            />
            )}
        </div>
        </div>
    );
}

function Section({ title, items, expanded, onToggle }) {
    return (
        <div className="border rounded-lg">
        <button
            onClick={onToggle}
            className="w-full p-4 text-left flex justify-between items-center hover:bg-gray-50"
        >
            <span className="font-semibold">{title}</span>
            <span>{expanded ? '−' : '+'}</span>
        </button>
        {expanded && (
            <div className="p-4 pt-0 space-y-2">
            {items.map((item, idx) => (
                <div key={idx} className="flex items-start space-x-2">
                <span className="text-blue-600 mt-1">•</span>
                <span>{item}</span>
                </div>
            ))}
            </div>
        )}
        </div>
    );
}

export default ScenarioCard;