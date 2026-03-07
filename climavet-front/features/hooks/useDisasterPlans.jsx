import { useState } from "react";
import axios from "axios";

function useDisasterPlans() {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchPlans = async (risk) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`/api/disaster-plans/?risk=${risk}`);
            setPlans(response.data);
        } catch (err) {
            setError(err.message || "An error occurred while fetching disaster plans.");
        } finally {
            setLoading(false);
        }
    };

    return { plans, loading, error, fetchPlans };
}

export default useDisasterPlans;