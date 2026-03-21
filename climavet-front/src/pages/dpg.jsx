// src/pages/PlanTypeSelector.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Dpg = () => {
    const navigate = useNavigate();
    const [selectedType, setSelectedType] = useState(null);
    const [showDetails, setShowDetails] = useState(false);

    const plans = {
        generic: {
            title: 'Generic Plan',
            description: 'A standard template that works for any veterinary clinic',
            details: 'Perfect if you need a basic disaster plan quickly. The generic plan covers essential emergency procedures, staff evacuation, and basic resource management.',
            icon: '📋',
            color: 'blue'
        },
        customized: {
            title: 'Customized Plan',
            description: 'Tailored to your clinic\'s specific needs, location, and risks',
            details: 'Ideal for clinics that want comprehensive coverage. The customized plan considers your clinic type, services, species treated, location risks, and available resources to create a detailed, actionable plan.',
            icon: '🎯',
            color: 'purple'
        }
    };

    const handleStart = () => {
        if (selectedType === 'generic') {
            navigate('/generic-disaster-plans');
        } else if (selectedType === 'customized') {
            navigate('/custom-disaster-plans');
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-4xl mx-auto py-12 px-4">
                {/* Progress Indicator */}
                <div className="mb-8">
                    <div className="flex items-center justify-center space-x-2 text-sm">
                        <span className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center">
                            1
                        </span>
                        <div className="w-12 h-0.5 bg-gray-300"></div>
                        <span className="bg-gray-300 text-gray-600 rounded-full w-8 h-8 flex items-center justify-center">
                            2
                        </span>
                        <div className="w-12 h-0.5 bg-gray-300"></div>
                        <span className="bg-gray-300 text-gray-600 rounded-full w-8 h-8 flex items-center justify-center">
                            3
                        </span>
                    </div>
                    <div className="flex justify-center mt-2 text-sm text-gray-500">
                        <span className="mx-6">Plan Type</span>
                        <span className="mx-6">Information</span>
                        <span className="mx-6">Generate</span>
                    </div>
                </div>

                {/* Header */}
                <div className="text-center mb-10">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Choose Your Plan Type
                    </h1>
                    <p className="text-gray-600">
                        Select how detailed you want your disaster plan to be
                    </p>
                </div>

                {/* Plan Options */}
                <div className="space-y-4 mb-8">
                    {Object.entries(plans).map(([type, plan]) => (
                        <div
                            key={type}
                            className={`
                                border rounded-lg transition-all cursor-pointer
                                ${selectedType === type
                                    ? `border-${plan.color}-500 ring-2 ring-${plan.color}-500 bg-${plan.color}-50`
                                    : 'border-gray-200 hover:border-gray-300 bg-white'
                                }
                            `}
                            onClick={() => {
                                setSelectedType(type);
                                setShowDetails(false);
                            }}
                        >
                            <div className="p-6">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-center space-x-4">
                                        <span className="text-3xl">{plan.icon}</span>
                                        <div>
                                            <h2 className="text-xl font-semibold text-gray-900">
                                                {plan.title}
                                            </h2>
                                            <p className="text-gray-600 mt-1">
                                                {plan.description}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex-shrink-0">
                                        <div className={`
                                            w-5 h-5 rounded-full border-2
                                            ${selectedType === type
                                                ? `bg-${plan.color}-500 border-${plan.color}-500`
                                                : 'border-gray-300'
                                            }
                                        `}>
                                            {selectedType === type && (
                                                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                                </svg>
                                            )}
                                        </div>
                                    </div>
                                </div>
                                
                                {selectedType === type && !showDetails && (
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setShowDetails(true);
                                        }}
                                        className="mt-4 text-sm text-blue-600 hover:text-blue-700"
                                    >
                                        Learn more about this plan →
                                    </button>
                                )}
                                
                                {selectedType === type && showDetails && (
                                    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                                        <p className="text-gray-700 text-sm">{plan.details}</p>
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setShowDetails(false);
                                            }}
                                            className="mt-2 text-sm text-blue-600 hover:text-blue-700"
                                        >
                                            Show less
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Action Buttons */}
                <div className="flex justify-between">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleStart}
                        disabled={!selectedType}
                        className={`
                            px-6 py-2 rounded-lg font-medium
                            ${selectedType
                                ? 'bg-blue-600 text-white hover:bg-blue-700'
                                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            }
                        `}
                    >
                        Start Planning →
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Dpg;