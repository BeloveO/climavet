import { useState, useEffect } from "react";
import axios from "axios";


const useClinicTypes = () => {
    const [clinicTypes, setClinicTypes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("/api/clinics/clinic-types")
        .then(response => setClinicTypes(response.data))
        .catch(err => setError(err.response?.data?.message || "Failed to fetch clinic types"))
        .finally(() => setLoading(false));
    }, []);

    return { clinicTypes, loading, error };
};

const useServiceTypes = () => {
    const [serviceTypes, setServiceTypes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("/api/clinics/service-types")
        .then(response => setServiceTypes(response.data))
        .catch(err => setError(err.response?.data?.message || "Failed to fetch service types"))
        .finally(() => setLoading(false));
    }, []);

    return { serviceTypes, loading, error };
};

const useSpeciesTypes = () => {
    const [speciesTypes, setSpeciesTypes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("/api/clinics/species-types")
        .then(response => setSpeciesTypes(response.data))
        .catch(err => setError(err.response?.data?.message || "Failed to fetch species types"))
        .finally(() => setLoading(false));
    }, []);

    return { speciesTypes, loading, error };
};

export { useClinicTypes, useServiceTypes, useSpeciesTypes };