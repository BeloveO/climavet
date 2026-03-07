import { useState, useEffect } from "react";
import { useSelector } from "react-redux";

const useDisasterPlan = (disasterPlanId) => {
    const [disasterPlan, setDisasterPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const clinicId = useSelector((state) => state.clinic.id);

    useEffect(() => {
        if (disasterPlanId) {
            fetch(`/api/disaster-plans/${disasterPlanId}?clinic_id=${clinicId}`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch disaster plan");
                    }
                    return response.json();
                })
                .then((data) => {
                    setDisasterPlan(data);
                    setLoading(false);
                })
                .catch((err) => {
                    setError(err.message || "Failed to fetch disaster plan");
                    setLoading(false);
                });
        }
    }, [disasterPlanId, clinicId]);

    return { disasterPlan, loading, error };
};

export default useDisasterPlan;