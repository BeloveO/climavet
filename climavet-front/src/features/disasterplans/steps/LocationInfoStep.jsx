

const PROVINCES = [
  { value: 'AB', label: 'Alberta' },
  { value: 'BC', label: 'British Columbia' },
  { value: 'MB', label: 'Manitoba' },
  { value: 'NB', label: 'New Brunswick' },
  { value: 'NL', label: 'Newfoundland and Labrador' },
  { value: 'NS', label: 'Nova Scotia' },
  { value: 'ON', label: 'Ontario' },
  { value: 'PE', label: 'Prince Edward Island' },
  { value: 'QC', label: 'Quebec' },
  { value: 'SK', label: 'Saskatchewan' },
  { value: 'NT', label: 'Northwest Territories' },
  { value: 'NU', label: 'Nunavut' },
  { value: 'YT', label: 'Yukon' }
];

const LocationInfoStep = ({ data, onUpdate, onNext, onBack }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    onNext();
  };

  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
        <div>
            <label className="block text-sm font-medium mb-2">
            Clinic Location (City, Address)
            </label>
            <input
            type="text"
            value={data.location}
            onChange={e => onUpdate({ location: e.target.value })}
            className="w-full border rounded-lg p-2"
            placeholder="e.g., Edmonton, AB"
            required
            />
        </div>
        <div>
            <label className="block text-sm font-medium mb-2">
                Province/Territory
            </label>
            <select
            value={data.province}
            onChange={e => onUpdate({ province: e.target.value })}
            className="w-full border rounded-lg p-2"
            required
            >
                <option value="">Select province...</option>
                {PROVINCES.map(prov => (
                    <option key={prov.code} value={prov.code}>
                    {prov.name}
                    </option>
                ))}
            </select>
        </div>
        <div className="border rounded-lg p-4 space-y-4">
            <h3 className="font-medium">Environmental Risk Factors</h3>
            <p className="text-sm text-gray-600">
                Select any risks that apply to your location:
            </p>
            
            <label className="flex items-center space-x-2">
                <input
                    type="checkbox"
                    checked={data.is_flood_zone}
                    onChange={e => onUpdate({ is_flood_zone: e.target.checked })}
                    className="rounded"
                />
                <span>Located in flood zone or near water bodies</span>
            </label>
            <label className="flex items-center space-x-2">
                <input
                    type="checkbox"
                    checked={data.is_wildfire_zone}
                    onChange={e => onUpdate({ is_wildfire_zone: e.target.checked })}
                    className="rounded"
                />
                <span>In or near wildfire-prone area (forest/grassland interface)</span>
            </label>
            <label className="flex items-center space-x-2">
                <input
                    type="checkbox"
                    checked={data.is_earthquake_zone}
                    onChange={e => onUpdate({ is_earthquake_zone: e.target.checked })}
                    className="rounded"
                />
                <span>In seismically active zone</span>
            </label>
        </div>
        <div className="flex space-x-4">
            <button
            type="button"
            onClick={onBack}
            className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400"
            >
                Back
            </button>
            <button
            type="submit"
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
            >
                Next: Review
            </button>
        </div>
    </form>
  );
}

export default LocationInfoStep;