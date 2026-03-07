// src/features/disaster-plan/DisasterPlanGenerator.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ClinicInfoStep } from './steps/ClinicInfoStep';
import { LocationInfoStep } from './steps/LocationStep';
import { ReviewInfoStep } from './steps/ReviewStep';
import { useDisasterPlan } from './hooks/useDisasterPlan';

export function DisasterPlanGenerator() {
  const [currentStep, setCurrentStep] = useState(1);
  const [planData, setPlanData] = useState({
    clinic_id: '',
    facility_type: null,
    service_types: [],
    species_treated: [],
    location: '',
    province: '',
    is_flood_zone: false,
    is_wildfire_zone: false,
    is_earthquake_zone: false,
  });
  
  const { generatePlan, isLoading } = useDisasterPlan();
  const navigate = useNavigate();
  
  const updatePlanData = (data) => {
    setPlanData(prev => ({ ...prev, ...data }));
  };
  
  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(prev => prev + 1);
    }
  };
  
  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1);
    }
  };
  
  const handleSubmit = async () => {
    const plan = await generatePlan(planData);
    if (plan) {
      navigate(`/disaster-plans/${plan.id}`);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">
        Disaster Plan Generator
      </h1>
      
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center">
          {[1, 2, 3].map(step => (
            <div key={step} className="flex items-center flex-1">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center
                ${currentStep >= step ? 'bg-blue-600 text-white' : 'bg-gray-300'}
              `}>
                {step}
              </div>
              {step < 3 && (
                <div className={`
                  flex-1 h-1 mx-2
                  ${currentStep > step ? 'bg-blue-600' : 'bg-gray-300'}
                `} />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-2">
          <span className="text-sm">Clinic Info</span>
          <span className="text-sm">Location & Risks</span>
          <span className="text-sm">Review & Generate</span>
        </div>
      </div>
      
      {/* Steps */}
      {currentStep === 1 && (
        <ClinicInfoStep
          data={planData}
          onUpdate={updatePlanData}
          onNext={handleNext}
        />
      )}
      
      {currentStep === 2 && (
        <LocationInfoStep
          data={planData}
          onUpdate={updatePlanData}
          onNext={handleNext}
          onBack={handleBack}
        />
      )}
      
      {currentStep === 3 && (
        <ReviewInfoStep
          data={planData}
          onBack={handleBack}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      )}
    </div>
  );
}