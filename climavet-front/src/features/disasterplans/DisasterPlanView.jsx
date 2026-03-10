import { useParams } from "react-router-dom";
import ScenarioCard from "./components/ScenarioCard";
import { useDisasterPlan } from "./hooks/useDisasterPlan";

function DisasterPlanView() {
    const { id } = useParams();
    const { plan, isLoading, downloadPDF } = useDisasterPlan(id);
    
    if (isLoading) return <div>Loading plan...</div>;
    if (!plan) return <div>Plan not found</div>;
    
    return (
        <div className="max-w-6xl mx-auto p-6">
        <div className="flex justify-between items-start mb-6">
            <div>
            <h1 className="text-3xl font-bold">
                Disaster Plan for {plan.clinic.name}
            </h1>
            <p className="text-gray-600 mt-2">
                {plan.location} • Generated {new Date(plan.created_at).toLocaleDateString()}
            </p>
            </div>
            
            <button
            onClick={downloadPDF}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
            📄 Download PDF
            </button>
        </div>
        
        {/* Risk Score */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Overall Risk Assessment</h2>
            <div className="flex items-center space-x-4">
            <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div
                    className={`h-full ${
                    plan.risk_score >= 70 ? 'bg-red-500' :
                    plan.risk_score >= 40 ? 'bg-yellow-500' :
                    'bg-green-500'
                    }`}
                    style={{ width: `${plan.risk_score}%` }}
                />
                </div>
            </div>
            <span className="text-2xl font-bold">{plan.risk_score}/100</span>
            </div>
        </div>
        
        {/* Scenarios */}
        <div className="space-y-6">
            <h2 className="text-2xl font-semibold">Disaster Scenarios</h2>
            {plan.scenarios.map(scenario => (
            <ScenarioCard key={scenario.id} scenario={scenario} />
            ))}
        </div>
        </div>
    );
}

export default DisasterPlanView;