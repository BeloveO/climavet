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
          Clinic Type
        </label>
        <select
          value={data.clinic_type || ''}
          onChange={(e) => onUpdate({ clinic_type: e.target.value })}
          className="w-full border rounded-lg p-2"
          required
        >
          <option value="">Select clinic type...</option>
          {clinicTypes.map((type) => (
            <option key={type.id} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>
      
      <div>
        <label className="block text-sm font-medium mb-2">
          Service Type
        </label>
        <select
          value={data.service_type || ''}
          onChange={(e) => onUpdate({ service_type: e.target.value })}
          className="w-full border rounded-lg p-2"
          required
        >
          <option value="">Select service type...</option>
          {serviceTypes.map((service) => (
            <option key={service.id} value={service.value}>
              {service.label}
            </option>
          ))}
        </select>
      </div>
      
      <div>
        <label className="block text-sm font-medium mb-2">
          Species Type
        </label>
        <select
          value={data.species_type || ''}
          onChange={(e) => onUpdate({ species_type: e.target.value })}
          className="w-full border rounded-lg p-2"
          required
        >
          <option value="">Select species type...</option>
          {speciesTypes.map((species) => (
            <option key={species.id} value={species.value}>
              {species.label}
            </option>
          ))}
        </select>
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