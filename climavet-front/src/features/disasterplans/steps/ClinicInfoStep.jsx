import { useServiceTypes, useClinicTypes, useSpeciesTypes } from '../hooks/useMetaData';



const ClinicInfoStep = ({ data, onNext, onUpdate }) => {
    const { clinicTypes } = useClinicTypes();
    const { serviceTypes } = useServiceTypes();
    const { speciesTypes } = useSpeciesTypes();
    
    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const clinicData = {
            clinic_id: formData.get('clinic_id'),
            clinic_type: formData.get('clinic_type'),
            service_types: formData.getAll('service_types'),
            species_treated: formData.getAll('species_treated'),
        };
        onNext(clinicData);
    }; 

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label className="block text-sm font-medium mb-2">
                    Facility Type
                </label>
                <select
                    value={data.facility_type || ''}
                    onChange={e => onUpdate({ facility_type: parseInt(e.target.value) })}
                    className="w-full border rounded-lg p-2"
                    required
                >
                    <option value="">Select facility type...</option>
                    {clinicTypes.map(type => (
                        <option key={type.id} value={type.id}>
                            {type.name}
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
                checked={data.service_types.includes(service.id)}
                onChange={e => {
                  const newServices = e.target.checked
                    ? [...data.service_types, service.id]
                    : data.service_types.filter(id => id !== service.id);
                  onUpdate({ service_types: newServices });
                }}
                className="rounded"
              />
              <span>{service.name}</span>
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
                checked={data.species_treated.includes(species.id)}
                onChange={e => {
                  const newSpecies = e.target.checked
                    ? [...data.species_treated, species.id]
                    : data.species_treated.filter(id => id !== species.id);
                  onUpdate({ species_treated: newSpecies });
                }}
                className="rounded"
              />
              <span>{species.name}</span>
            </label>
          ))}
        </div>
      </div>
      
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
      >
        Next: Location & Risks
      </button>
    </form>
  );
}

export default ClinicInfoStep;