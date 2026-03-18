import ClinicInfoStep from './ClinicInfoStep';
import LocationInfoStep from './LocationInfoStep';

const ReviewInfoStep = ({ planData }) => {
    return (
        <div className="space-y-6">
            <h2 className="text-xl font-semibold">Review Your Information</h2>
            <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="text-lg font-medium">Clinic Information</h3>
                <p><strong>Clinic ID:</strong> {planData.clinic_id}</p>
                <p><strong>Facility Type:</strong> {planData.clinic_type}</p>
                <p><strong>Service Types:</strong> {planData.service_types.join(', ')}</p>
                <p><strong>Species Treated:</strong> {planData.species_treated.join(', ')}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="text-lg font-medium">Location Information</h3>
                <p><strong>Location:</strong> {planData.location}</p>
                <p><strong>Province:</strong> {planData.province}</p>
                <p><strong>Flood Zone:</strong> {planData.is_flood_zone ? 'Yes' : 'No'}</p>
                <p><strong>Wildfire Zone:</strong> {planData.is_wildfire_zone ? 'Yes' : 'No'}</p>
                <p><strong>Earthquake Zone:</strong> {planData.is_earthquake_zone ? 'Yes' : 'No'}</p>
            </div>
        </div>
    );
};

export default ReviewInfoStep;