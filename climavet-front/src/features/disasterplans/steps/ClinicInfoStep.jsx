// src/features/disaster-plan/steps/ClinicInfoStep.jsx
import { useClinicTypes, useServiceTypes, useSpeciesTypes } from '../hooks/useMetaData';

const ClinicInfoStep = ({ data, onUpdate, onNext }) => {
    const { clinicTypes } = useClinicTypes();
    const { serviceTypes } = useServiceTypes();
    const { speciesTypes } = useSpeciesTypes();

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('ClinicInfoStep - Submitting with data:', data);
        onNext();
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label className="block text-sm font-medium mb-2">
                    Clinic Type
                </label>
                <select
                    value={data.clinic_type || ''}
                    onChange={e => {
                        onUpdate({ clinic_type: e.target.value });
                    }}
                    className="w-full border rounded-lg p-2"
                    required
                >
                    <option value="">Select Clinic type...</option>
                    {clinicTypes.map(type => (
                        <option key={type.id} value={type.id}>
                            {type.label}
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block text-sm font-medium mb-2">
                    Services Provided (select all that apply)
                </label>
                <div className="space-y-2 max-h-60 overflow-y-auto border rounded-lg p-4">
                    {serviceTypes.map(service => (
                        <label key={service.id} className="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                checked={data.service_types?.includes(service.id) || false}
                                onChange={e => {
                                    const newServices = e.target.checked
                                        ? [...(data.service_types || []), service.id]
                                        : (data.service_types || []).filter(id => id !== service.id);
                                    console.log('Updated service types:', newServices);
                                    onUpdate({ service_types: newServices });
                                }}
                                className="rounded"
                            />
                            <span>{service.label}</span>
                        </label>
                    ))}
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium mb-2">
                    Species Treated (select all that apply)
                </label>
                <div className="space-y-2 max-h-60 overflow-y-auto border rounded-lg p-4">
                    {speciesTypes.map(species => (
                        <label key={species.id} className="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                checked={data.species_types?.includes(species.id) || false}
                                onChange={e => {
                                    const newSpecies = e.target.checked
                                        ? [...(data.species_types || []), species.id]
                                        : (data.species_types || []).filter(id => id !== species.id);
                                    console.log('Updated species:', newSpecies);
                                    onUpdate({ species_types: newSpecies });
                                }}
                                className="rounded"
                            />
                            <span>{species.label}</span>
                        </label>
                    ))}
                </div>
            </div>

            <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
            >
                Next: Location & Risks →
            </button>
        </form>
    );
};

export default ClinicInfoStep;