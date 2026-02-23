import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, Button, CircularProgress } from '@mui/material';
import { CheckCircle } from '@mui/icons-material';


function Dpg() {
    const [disasterTypes, setDisasterTypes] = useState([]);
    const [selectedDisasterType, setSelectedDisasterType] = useState('');
    const [generating, setGeneratingPlan] = useState(null);
    const [plan, setPlan] = useState(null);
    const [loading, setLoading] = useState(false);
    const [editMode, setEditMode] = useState(false);
    const [error, setError] = useState(null);
    const steps = [
        'Select Disaster Type',
        'Generating Plan',
        'Review & Finalize'
    ];

    useEffect(() => {
        // Fetch disaster types from the backend
        axios.get('/api/disaster-plans/types/')
            .then(response => {
                setDisasterTypes(response.data);
            })
            .catch(error => {
                console.error('Error fetching disaster types:', error);
                setError('Failed to load disaster types. Please try again later.');
            });
    }, []);

    const handleGeneratePlan = () => {
        if (!selectedDisasterType) {
            setError('Please select a disaster type before generating a plan.');
            return;
        }
        setError(null);
        setGeneratingPlan(true);
        setLoading(true);
        console.log('Selected disaster type ID:', selectedDisasterType);

        // Function to get CSRF token from cookies
        // function getCookie(name) {
        //    let cookieValue = null;
        //    if (document.cookie && document.cookie !== '') {
        //        const cookies = document.cookie.split(';');
        //       for (let i = 0; i < cookies.length; i++) {
        //            const cookie = cookies[i].trim();
        //            // Does this cookie string begin with the name we want?
        //            if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                break;
        //            }
        //        }
        //    }
        //    return cookieValue;
        //}
        
        //const csrftoken = getCookie('csrftoken');


        axios.get('/api/disaster-plans/plans/generate/', {
            params: {
                disaster_type: selectedDisasterType
            },
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                console.log('Generated plan:', response.data);
                setPlan(response.data);
                setGeneratingPlan(false);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error generating disaster plan:', error);
                setError('Failed to generate disaster plan. Please try again later.');
                setGeneratingPlan(false);
                setLoading(false);
            });
    };

    const handleEditPlan = () => {
        setEditMode(true);
    };

    const handleSavePlan = () => {
        // Implement save functionality here (e.g., send updated plan to backend)
        setEditMode(false);
    };

    const renderStepIndicator = () => {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                {steps.map((step, index) => (
                    <div key={index} style={{ display: 'flex', alignItems: 'center', marginRight: '20px' }}>
                        <div
                            style={{
                                width: '30px',
                                height: '30px',
                                borderRadius: '50%',
                                backgroundColor: index <= (generating ? 1 : 0) ? '#4caf50' : '#ccc',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: '#fff',
                                fontWeight: 'bold'
                            }}
                        >
                            {index + 1}
                        </div>
                        <Typography variant="body1" style={{ marginLeft: '8px' }}>
                            {step}
                        </Typography>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <Container maxWidth="md" style={{ marginTop: '40px' }}>
            <Typography variant="h4" gutterBottom>
                Disaster Plan Generator
            </Typography>
            {renderStepIndicator()}
            {error && <Typography color="error">{error}</Typography>}
            {!generating && (
                <>
                    <Typography variant="h6" gutterBottom>
                        Select Disaster Type
                    </Typography>
                    <select
                        value={selectedDisasterType}
                        onChange={(e) => setSelectedDisasterType(e.target.value)}
                        style={{ padding: '10px', fontSize: '16px', width: '100%', marginBottom: '20px' }}
                    >
                        <option value="">-- Select a Disaster Type --</option>
                        {disasterTypes.map((type) => (
                            <option key={type.id} value={type.id}>
                                {type.name}
                            </option>
                        ))}
                    </select>
                    <Button variant="contained" color="primary" onClick={handleGeneratePlan} disabled={!selectedDisasterType}>
                        Generate Plan
                    </Button>
                </>
            )}
            {loading && (
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                    <CircularProgress />
                </div>
            )}
            {plan && !editMode && (
                <div style={{ marginTop: '30px' }}>
                    <Typography variant="h5" gutterBottom>
                        {plan.name || 'Generated Disaster Plan'}
                    </Typography>
                    {plan.description && (
                    <Typography variant="body1" style={{ marginBottom: '20px', fontStyle: 'italic' }}>
                        {plan.description}
                    </Typography>
                    )}
                    {/* Common Regions */}
                    {plan.common_regions && plan.common_regions.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Commonly Affected Regions
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.common_regions.map((region, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        {region}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                     {/* Preparation Steps */}
                    {plan.preparation_steps && plan.preparation_steps.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Preparation Steps
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.preparation_steps.map((step, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        {step}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    
                    {/* Response Steps */}
                    {plan.response_steps && plan.response_steps.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Response Steps
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.response_steps.map((step, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        {step}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    
                    {/* Recovery Steps */}
                    {plan.recovery_steps && plan.recovery_steps.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Recovery Steps
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.recovery_steps.map((step, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        {step}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    {/* Emergency Contacts */}
                    {plan.emergency_contacts && plan.emergency_contacts.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Emergency Contacts
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.emergency_contacts.map((contact, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        <strong>{contact.name}:</strong> {contact.phone} ({contact.type})
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    
                    {/* Supplies Needed */}
                    {plan.supplies_needed && plan.supplies_needed.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Supplies Needed
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.supplies_needed.map((supply, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        <strong>{supply.item}:</strong> {supply.quantity} {supply.unit}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                
                    {/* Training Requirements */}
                    {plan.training_requirements && plan.training_requirements.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            <Typography variant="h6" gutterBottom>
                                Training Requirements
                            </Typography>
                            <ul style={{ paddingLeft: '20px' }}>
                                {plan.training_requirements.map((training, index) => (
                                    <li key={index} style={{ marginBottom: '8px' }}>
                                        {training}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    <Button variant="outlined" color="primary" onClick={handleEditPlan} style={{ marginRight: '10px' }}>
                        Edit Plan
                    </Button>
                    <Button variant="contained" color="primary" onClick={handleSavePlan}>
                        Save Plan
                    </Button>
                </div>
            )}
            {editMode && (
                <div style={{ marginTop: '30px' }}>
                    <Typography variant="h5" gutterBottom>
                        Edit Disaster Plan
                    </Typography>
                    <textarea
                        value={plan.plan_text}
                        onChange={(e) => setPlan({ ...plan, plan_text: e.target.value })}
                        style={{ width: '100%', height: '300px', padding: '10px', fontSize: '16px' }}
                    />
                    <Button variant="contained" color="primary" onClick={handleSavePlan} style={{ marginTop: '20px' }}>
                        Save Changes
                    </Button>
                </div>
            )}
        </Container>
    );
}
export default Dpg