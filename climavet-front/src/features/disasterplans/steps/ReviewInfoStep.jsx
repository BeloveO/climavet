// src/features/disaster-plan/steps/ReviewInfoStep.jsx
import { useClinicTypes, useServiceTypes, useSpeciesTypes } from '../hooks/useMetaData';

const ReviewInfoStep = ({ planData = {}, onBack, onSubmit, isLoading }) => {

    console.log('ReviewInfoStep - planData:', planData);
    // Fetch metadata to convert IDs to names
    const { clinicTypes = [], isLoading: loadingClinics } = useClinicTypes();
    const { serviceTypes = [], isLoading: loadingServices } = useServiceTypes();
    const { speciesTypes = [], isLoading: loadingSpecies } = useSpeciesTypes();

    // Check if still loading metadata
    const isLoadingMetadata = loadingClinics || loadingServices || loadingSpecies;

    // Safely access planData properties with default values
    const {
        clinic_type = null,
        service_types = [],
        species_types = [],
        address = '',
        province = '',
        city = '',
        is_flood_zone = false,
        is_wildfire_zone = false,
        is_earthquake_zone = false
    } = planData;

    // Helper functions to convert IDs to names with safety checks
    const getClinicTypeName = () => {
        if (!clinicTypes || clinicTypes.length === 0) return 'Loading...';
        const clinic = clinicTypes.find(f => String(f.id) === String(clinic_type));
        return clinic?.label || clinic?.name || 'Not selected';
    }

    const getServiceTypeNames = () => {
        if (!serviceTypes || serviceTypes.length === 0) return 'Loading...';
        if (!service_types || service_types.length === 0) return 'None selected';
        
        const names = serviceTypes
            .filter(s => service_types.includes(s.id))
            .map(s => s.label)
            .join(', ');
        return names || 'None selected';
    };

    const getSpeciesNames = () => {
        if (!speciesTypes || speciesTypes.length === 0) return 'Loading...';
        if (!species_types || species_types.length === 0) return 'None selected';
        
        const names = speciesTypes
            .filter(s => species_types.includes(s.id))
            .map(s => s.label)
            .join(', ');
        return names || 'None selected';
    };

    // Show loading state while fetching metadata
    if (isLoadingMetadata) {
        return (
            <div className="space-y-6">
                <h2 className="text-2xl font-bold mb-2">Review Your Information</h2>
                <div className="flex items-center justify-center py-12">
                    <div className="text-center">
                        <svg className="animate-spin h-10 w-10 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <p className="text-gray-600">Loading information...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold mb-2">Review Your Information</h2>
                <p className="text-gray-600">
                    Please verify all information is correct before generating your disaster plan.
                </p>
            </div>

            {/* Clinic Information Section */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-4">
                    🏥 Clinic Information
                </h3>
                <dl className="space-y-3">
                    <div>
                        <dt className="text-sm font-medium text-gray-600">Clinic Type</dt>
                        <dd className="mt-1 text-gray-900">{getClinicTypeName()}</dd>
                    </div>
                    <div>
                        <dt className="text-sm font-medium text-gray-600">Services Provided</dt>
                        <dd className="mt-1 text-gray-900">{getServiceTypeNames()}</dd>
                    </div>
                    <div>
                        <dt className="text-sm font-medium text-gray-600">Species Treated</dt>
                        <dd className="mt-1 text-gray-900">{getSpeciesNames()}</dd>
                    </div>
                </dl>
            </div>

            {/* Location Information Section */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-green-900 mb-4">
                    📍 Location & Risk Factors
                </h3>
                <dl className="space-y-3">
                    <div>
                        <dt className="text-sm font-medium text-gray-600">Address</dt>
                        <dd className="mt-1 text-gray-900">{address || 'Not provided'}</dd>
                    </div>
                    <div>
                        <dt className=""text-sm font-medium text-gray-600>City</dt>
                        <dd className="mt-1 text-gray-900">{city || 'Not provided'}</dd>
                    </div>
                    <div>
                        <dt className="text-sm font-medium text-gray-600">Province/Territory</dt>
                        <dd className="mt-1 text-gray-900">{province || 'Not selected'}</dd>
                    </div>
                    <div className="pt-2 border-t border-green-200">
                        <dt className="text-sm font-medium text-gray-600 mb-2">Environmental Risks</dt>
                        <dd className="space-y-2">
                            <div className="flex items-center">
                                <span className={`w-4 h-4 rounded-full mr-2 ${is_flood_zone ? 'bg-blue-500' : 'bg-gray-300'}`}></span>
                                <span className="text-gray-900">Flood Zone</span>
                            </div>
                            <div className="flex items-center">
                                <span className={`w-4 h-4 rounded-full mr-2 ${is_wildfire_zone ? 'bg-orange-500' : 'bg-gray-300'}`}></span>
                                <span className="text-gray-900">Wildfire Zone</span>
                            </div>
                            <div className="flex items-center">
                                <span className={`w-4 h-4 rounded-full mr-2 ${is_earthquake_zone ? 'bg-yellow-500' : 'bg-gray-300'}`}></span>
                                <span className="text-gray-900">Earthquake Zone</span>
                            </div>
                        </dd>
                    </div>
                </dl>
            </div>

            {/* Warning if no risks selected */}
            {!is_flood_zone && !is_wildfire_zone && !is_earthquake_zone && (
                <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-4">
                    <div className="flex">
                        <span className="text-yellow-600 mr-2">⚠️</span>
                        <div>
                            <h4 className="font-medium text-yellow-900">No Environmental Risks Selected</h4>
                            <p className="text-sm text-yellow-700 mt-1">
                                Your disaster plan will be generated based on your province/territory's 
                                typical climate risks. Consider going back to select specific risks if known.
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex gap-4 pt-4">
                <button
                    type="button"
                    onClick={onBack}
                    disabled={isLoading}
                    className="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    ← Back
                </button>
                <button
                    type="button"
                    onClick={onSubmit}
                    disabled={isLoading}
                    className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {isLoading ? (
                        <span className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Generating Plan...
                        </span>
                    ) : (
                        '✓ Generate Disaster Plan'
                    )}
                </button>
            </div>

            {/* What happens next */}
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-600">
                <p className="font-medium text-gray-900 mb-2">What happens next?</p>
                <ul className="space-y-1 ml-4">
                    <li>• We'll analyze your clinic's specific vulnerabilities</li>
                    <li>• Generate customized disaster scenarios and action plans</li>
                    <li>• Create species-specific evacuation protocols</li>
                    <li>• Provide equipment protection guidelines</li>
                    <li>• Generate a comprehensive resource checklist</li>
                </ul>
            </div>
        </div>
    );
};

export default ReviewInfoStep;