// src/features/disaster-plan/hooks/useDisasterPlan.ts
import { useState } from 'react';
import axios from 'axios';


const useDisasterPlan = (planId = undefined) => {
  const [plan, setPlan] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const generatePlan = async (data) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/disaster-plans/plans/', data);
      setPlan(response.data);
      return response.data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setIsLoading(false);
    }
  };
  
  const downloadPDF = async () => {
    try {
      const response = await axios.get(
        `/api/disaster-plans/${planId}/download_pdf/`,
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `disaster-plan-${planId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('PDF download failed:', err);
    }
  };
  
  return {
    plan,
    isLoading,
    error,
    generatePlan,
    downloadPDF
  };
}

export { useDisasterPlan };