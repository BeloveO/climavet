// src/pages/PlanTypeSelector.jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Footer from './footer.jsx';


const PLANS = {
    generic: {
        title: 'Generic Plan',
        description: 'A standard template that works for any veterinary clinic',
        details: 'Perfect if you need a basic disaster plan quickly. The generic plan covers essential emergency procedures, staff evacuation, and basic resource management.',
        icon: (
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
        ),
        badge: 'Quick Start',
        styles: {
            card: 'border-emerald-600 ring-2 ring-emerald-600 bg-emerald-50/60',
            iconWrap: 'bg-emerald-100 text-emerald-700',
            radio: 'border-emerald-600 bg-emerald-600',
            badge: 'bg-emerald-100 text-emerald-800',
            button: 'text-emerald-700 hover:text-emerald-800',
            detailBox: 'bg-white ring-1 ring-emerald-100',
        }
    },
    customized: {
        title: 'Customized Plan',
        description: 'Tailored to your clinic\'s specific needs, location, and risks',
        details: 'Ideal for clinics that want comprehensive coverage. The customized plan considers your clinic type, services, species treated, location risks, and available resources to create a detailed, actionable plan.',
        icon: (
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
        ),
        badge: 'Detailed',
        styles: {
            card: 'border-emerald-600 ring-2 ring-emerald-600 bg-emerald-50/60',
            iconWrap: 'bg-emerald-100 text-emerald-700',
            radio: 'border-emerald-600 bg-emerald-600',
            badge: 'bg-emerald-100 text-emerald-800',
            button: 'text-emerald-700 hover:text-emerald-800',
            detailBox: 'bg-white ring-1 ring-emerald-100',
        }
    }
}

const STEPS = ['Plan Type', 'Information', 'Generate']

const DEFAULT_STYLES = {
    card: 'border-slate-200 bg-white hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md',
    iconWrap: 'bg-slate-100 text-slate-600',
    radio: 'border-slate-300 bg-white',
    badge: 'bg-slate-100 text-slate-600',
    button: 'text-emerald-700 hover:text-emerald-800',
    detailBox: 'bg-slate-50 ring-1 ring-slate-200',
}

const PlanTypeSelector = () => {
    const navigate = useNavigate();
    const [selectedType, setSelectedType] = useState(null);
    const [showDetails, setShowDetails] = useState(false);

    const handleStart = () => {
        if (selectedType === 'generic') {
            navigate('/generic-disaster-plans');
        } else if (selectedType === 'customized') {
            navigate('/custom-disaster-plans');
        }
    };

    return (
        <div className="flex min-h-screen flex-col bg-white font-sans text-slate-900">
            <nav className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur">
                <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">
                    <Link to="/" className="flex items-center gap-2">
                        <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-700 text-lg font-bold text-white">
                            C
                        </span>
                        <span className="text-xl font-bold tracking-tight text-slate-900">ClimaVet</span>
                    </Link>

                    <div className="hidden items-center gap-8 md:flex">
                        <Link to="/" className="text-sm font-medium text-slate-600 transition hover:text-emerald-700">
                            Home
                        </Link>
                        <Link to="/dashboard" className="text-sm font-medium text-slate-600 transition hover:text-emerald-700">
                            Dashboard
                        </Link>
                    </div>

                    <button
                        onClick={() => navigate('/dashboard')}
                        className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                    >
                        Cancel
                    </button>
                </div>
            </nav>
            <main className="flex-1">
                { /* Hero Band */ }
                <section className="relative overflow-hidden bg-gradient-to-br from-emerald-900 via-emerald-800 to-teal-700 text-white">
                    <div className="absolute inset-0 opacity-10 [background-image:radial-gradient(circle_at_1px_1px,white_1px,transparent_0)] [background-size:24px_24px]" />
                    <div className="relative mx-auto max-w-7xl px-6 py-16 lg:px-8">
                        { /* Progress Indicator */ }
                        <ol className="flex items-center justify-center gap-3 text-sm font-medium">
                            {STEPS.map((label, index) => {
                                const isActive = index === 0; // Only the first step is active
                                return (
                                    <li key={label} className="flex items-center gap-3">
                                        <span 
                                            className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold ${
                                                isActive
                                                ? 'bg-white text-emerald-800'
                                                : 'bg-white/10 text-emerald-100 ring-1 ring-inset ring-white/20'
                                            }`}
                                        >
                                            {index + 1}
                                        </span>
                                        <span className={isActive ? 'font-semibold text-white' : 'text-emerald-100/80'}>
                                            {label}
                                        </span>
                                        {index < STEPS.length - 1 && <span className="mx-2 h-px w-10 bg-white/30" />}
                                    </li>
                                )
                            })}
                        </ol>
                        <div className="mx-auto mt-10 max-w-2xl text-center">
                            <span className="inline-flex items-center rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-emerald-100 ring-1 ring-inset ring-white/20">
                                Disaster Plan Generator
                            </span>
                            <h1 className="mt-6 text-4xl font-extrabold tracking-tight sm:text-5xl">
                                Choose Your Plan Type
                            </h1>
                            <p className="mt-4 text-lg leading-8 text-emerald-100">
                                Select how detailed you want your disaster plan to be. You can choose a generic plan for quick setup or a customized plan tailored to your clinic's specific needs.
                            </p>
                        </div>
                    </div>
                </section>

                { /* Plan Type Selection */ }
                <section className="mx-auto max-w-4xl px-6 py-16 lg:px-8">
                    <div className="space-y-6">
                        {Object.entries(PLANS).map(([type, plan]) => {
                            const isSelected = selectedType === type;
                            const styles = isSelected ? plan.styles : DEFAULT_STYLES;

                            return (
                                <div key={type} role='radio'
                                    aria-checked={isSelected}
                                    tabIndex={0}
                                    onClick={() => {
                                        setSelectedType(type);
                                        setShowDetails(false);
                                    }}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter' || e.key === ' ') {
                                            e.preventDefault();
                                            setSelectedType(type);
                                            setShowDetails(false);
                                        }
                                    }}
                                    className={`group cursor-pointer rounded-xl border p-6 shadow-sm transition focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${styles.card}`}
                                >
                                    <div className="flex items-start justify-between gap-6">
                                        <div className="flex items-start gap-5">
                                            <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-lg ${styles.iconWrap}`}>
                                                {plan.icon}
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-3">
                                                    <h2 className="text-xl font-semibold text-slate-900">{plan.title}</h2>
                                                    <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${styles.badge}`}>
                                                        {plan.badge}
                                                    </span>
                                                </div>
                                                <p className="mt-2 text-sm leading-6 text-slate-600">{plan.description}</p>
                                            </div>
                                        </div>

                                        { /* Radio Indicator */ }
                                        <div
                                            className={`mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 ${
                                                isSelected ? styles.radio : 'border-slate-300 bg-white'
                                            }`}
                                        >
                                            {isSelected && <span className="h-2 w-2 rounded-full bg-white" />}
                                        </div>
                                    </div>

                                    {isSelected && showDetails && (
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setShowDetails(false);
                                            }}
                                            className={`mt-5 text-sm font-semibold transition ${styles.button}`}
                                        >
                                            Learn more about this plan <span aria-hidden="true">&rarr;</span>
                                        </button>
                                    )}

                                    {isSelected && !showDetails && (
                                        <div className={`mt-5 rounded-lg p-4 ${styles.detailBox}`}>
                                            <p className="text-sm leading-6 text-slate-700">{plan.details}</p>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    setShowDetails(true);
                                                }}
                                                className={`mt-3 text-sm font-semibold transition ${styles.button}`}
                                            >
                                                Show less
                                            </button>
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                    
                    { /* Action */ }
                    <div className="mt-12 flex flex-col-reverse gap-4 border-t border-slate-200 pt-8 sm:flex-row sm:justify-between">
                        <button 
                            onClick={() => navigate('/dashboard')}
                            className="rounded-md border border-slate-300 px-6 py-3 text-center text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleStart}
                            disabled={!selectedType}
                            className={`rounded-md px-6 py-3 text-center text-sm font-semibold shadow-sm transition ${
                                selectedType
                                ? 'bg-emerald-700 text-white hover:bg-emerald-800'
                                : 'cursor-not-allowed bg-slate-200 text-slate-500'
                            }`}
                        >
                            Start Planning <span aria-hidden="true">&rarr;</span>
                        </button>
                    </div>
                </section>
            </main>

            { /* Footer */ }
            <Footer />
        </div>
    );
};

export default PlanTypeSelector;