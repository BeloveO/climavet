import { useState, useEffect } from "react";
import { useSelector } from "react-redux";

const useClinicTypes = () => {
    const [clinicTypes, setClinicTypes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const clinicId = useSelector((state) => state.clinic.id);

    useEffect(() => {
        if (clinicId) {
            fetch(`/api/clinic-types?clinic_id=${clinicId}`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch clinic types");
                    }
                    return response.json();
                })
                .then((data) => {
                    setClinicTypes(data);
                    setLoading(false);
                })
                .catch((err) => {
                    setError(err.message || "Failed to fetch clinic types");
                    setLoading(false);
                });
        }
    }, [clinicId]);

    return { clinicTypes, loading, error };
};

const useServiceTypes = () => {
    const [serviceTypes, setServiceTypes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const clinicId = useSelector((state) => state.clinic.id);

    useEffect(() => {
        if (clinicId) {
            fetch(`/api/service-types?clinic_id=${clinicId}`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch service types");
                    }
                    return response.json();
                })
                .then((data) => {
                    setServiceTypes(data);
                    setLoading(false);
                })
                .catch((err) => {
                    setError(err.message || "Failed to fetch service types");
                    setLoading(false);
                });
        }
    }, [clinicId]);

    return { serviceTypes, loading, error };
};

const useSpeciesTypes = () => {
    const [speciesTypes, setSpeciesTypes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const clinicId = useSelector((state) => state.clinic.id);

    useEffect(() => {
        if (clinicId) {
            fetch(`/api/species-types?clinic_id=${clinicId}`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch species types");
                    }
                    return response.json();
                })
                .then((data) => {
                    setSpeciesTypes(data);
                    setLoading(false);
                })
                .catch((err) => {
                    setError(err.message || "Failed to fetch species types");
                    setLoading(false);
                });
        }
    }, [clinicId]);

    return { speciesTypes, loading, error };
};

export { useClinicTypes, useServiceTypes, useSpeciesTypes };