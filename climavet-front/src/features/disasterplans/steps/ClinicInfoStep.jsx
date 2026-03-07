import { useState, useEffect } from 'react';
import { useServiceTypes, useClinicTypes, useSpeciesTypes } from './hooks/useMetaData';

const ClinicInfoStep = ({ onDataChange }) => {
    const { clinicTypes, loading: clinicTypesLoading } = useClinicTypes();
    const { serviceTypes, loading: serviceTypesLoading } = useServiceTypes();
    const { speciesTypes, loading: speciesTypesLoading } = useSpeciesTypes();
    
    const [clinicId, setClinicId] = useState('');
    const [facilityType, setFacilityType] = useState('');
    const [selectedServiceTypes, setSelectedServiceTypes] = useState([]);
    const [selectedSpecies, setSelectedSpecies] = useState([]);
    
    useEffect(() => {
        onDataChange({
            clinic_id: clinicId,
            facility_type: facilityType,
            service_types: selectedServiceTypes,
            species_treated: selectedSpecies,
        });
    }, [clinicId, facilityType, selectedServiceTypes, selectedSpecies]);
    
    if (clinicTypesLoading || serviceTypesLoading || speciesTypesLoading) {
        return <div>Loading...</div>;
    }
    
    return (
        <div className="space-y-6">
            <div>
                <label className="block text-sm font-medium text-gray-700">Clinic</label>
                <select
                    value={clinicId}
                    onChange={(e) => setClinicId(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                >
                    <option value="">Select a clinic</option>
                    {clinicTypes.map((clinic) => (
                        <option key={clinic.id} value={clinic.id}>
                            {clinic.name}
                        </option>
                    ))}
                </select>
            </div>
            
            <div>
                <label className="block text-sm font-medium text-gray-700">Facility Type</label>
                <select
                    value={facilityType}
                    onChange={(e) => setFacilityType(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                >
                    <option value="">Select facility type</option>
                    {clinicTypes.map((clinic) => (
                        <option key={clinic.id} value={clinic.facility_type}>
                            {clinic.facility_type}
                        </option>
                    ))}
                </select>
            </div>
            
            <div>
                <label className="block text-sm font-medium text-gray-700">Service Types</label>
                <select
                    multiple
                    value={selectedServiceTypes}
                    onChange={(e) => {
                        const options = Array.from(e.target.options);
                        const selected = options.filter(o => o.selected).map(o => o.value);
                        setSelectedServiceTypes(selected);
                    }}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                >
                    {serviceTypes.map((service) => (
                        <option key={service.id} value={service.id}>
                            {service.name}
                        </option>
                    ))}
                </select>
            </div>
            
            <div>
                <label className="block text-sm font-medium text-gray-700">Species Treated</label>
                <select
                    multiple
                    value={selectedSpecies}
                    onChange={(e) => {
                        const options = Array.from(e.target.options);
                        const selected = options.filter(o => o.selected).map(o => o.value);
                        setSelectedSpecies(selected);
                    }}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                >
                    {speciesTypes.map((species) => (
                        <option key={species.id} value={species.id}>
                            {species.name}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    );
};

export default ClinicInfoStep;