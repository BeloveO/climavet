import { useState } from "react";
import CheckListItem from "./componenets/CheckListItem";
import useChecklists from "./hooks/useChecklists";
import { useDisasterTypes } from "../disasterTypes/hooks/useDisasterTypes";
import { useNavigate } from "react-router-dom";

const CheckListBuilder = () => {
    const [formData, setFormData] = useState({
    clinic_id: '',
    name: '',
    description: '',
    disaster_types: [],
  });
  
  const { createChecklist, isLoading } = useChecklists();
  const { disasterTypes } = useDisasterTypes();
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const checklist = await createChecklist(formData);
    if (checklist) {
      navigate(`/checklists/${checklist.id}`);
    }
  };
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">
        Create Emergency Resource Checklist
      </h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">
            Checklist Name
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
            placeholder="e.g., Winter Emergency Supplies"
            className="w-full border rounded-lg p-2"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">
            Description (Optional)
          </label>
          <textarea
            value={formData.description}
            onChange={e => setFormData(prev => ({ ...prev, description: e.target.value }))}
            placeholder="What is this checklist for?"
            className="w-full border rounded-lg p-2 h-24"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">
            Select Disaster Types
          </label>
          <p className="text-sm text-gray-600 mb-3">
            Choose which disasters this checklist should prepare for. We'll generate
            appropriate supplies for each.
          </p>
          
          <div className="space-y-2 border rounded-lg p-4 max-h-80 overflow-y-auto">
            {disasterTypes.map(disaster => (
              <label key={disaster.id} className="flex items-start space-x-3 p-2 hover:bg-gray-50 rounded">
                <input
                  type="checkbox"
                  checked={formData.disaster_types.includes(disaster.id)}
                  onChange={e => {
                    const newTypes = e.target.checked
                      ? [...formData.disaster_types, disaster.id]
                      : formData.disaster_types.filter(id => id !== disaster.id);
                    setFormData(prev => ({ ...prev, disaster_types: newTypes }));
                  }}
                  className="mt-1"
                />
                <div>
                  <div className="font-medium">{disaster.name}</div>
                  <div className="text-sm text-gray-600">{disaster.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>
        
        <button
          type="submit"
          disabled={isLoading || formData.disaster_types.length === 0}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {isLoading ? 'Generating Checklist...' : 'Generate Checklist'}
        </button>
      </form>
    </div>
  );
}

export default CheckListBuilder;