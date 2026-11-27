import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Footer from '../../pages/footer'


const STEPS = ['Select Disaster Type', 'Generating Plan', 'Review & Finalize']

function Section({ title, children }) {
    return (
        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
            <div className="mt-4">{children}</div>
        </section>
    )
}

function BulletList({items, render}) {
    return (
        <ul className="space-y-3">
            {items.map((item, index) => (
                <li key={index} className="flex gap-3 text-sm leading-6 text-slate-700">
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-600" />
                    <span>{render ? render(item) : item}</span>
                </li>
            ))}
        </ul>
    )
}

function GenericDisasterPlans() {
    const [disasterTypes, setDisasterTypes] = useState([])
    const [selectedDisasterType, setSelectedDisasterType] = useState('')
    const [step, setStep] = useState(0) // 0 = select, 1 = generating, 2 = review
    const [plan, setPlan] = useState(null)
    const [loading, setLoading] = useState(false)
    const [editMode, setEditMode] = useState(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        // Fetch disaster types from the backend
        axios.get('/api/disaster-plans/types/')
            .then(response => {
                setDisasterTypes(response.data);
            })
            .catch(err => {
                console.error('Error fetching disaster types:', err);
                setError('Failed to load disaster types. Please try again later.');
            });
    }, []);

    const handleGeneratePlan = () => {
        if (!selectedDisasterType) {
            setError('Please select a disaster type before generating a plan.');
            return
        }
        setError(null)
        setStep(1)
        setLoading(true)


        axios.get('/api/disaster-plans/plans/generate/', {
            params: {
                disaster_type: selectedDisasterType
            },
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            setPlan(response.data)
            setStep(2)
        })
        .catch(err => {
            console.error('Error generating disaster plan:', err)
            setError('Failed to generate disaster plan. Please try again later.')
            setStep(0)
        })
        .finally(() => {
            setLoading(false)
        })
    }

    const handleStartOver = () => {
        setPlan(null)
        setEditMode(false)
        setSelectedDisasterType('')
        setStep(0)
        setError(null)
    }

    const handleSavePlan = () => {
        // Implement save functionality here (e.g., send updated plan to backend)
        setEditMode(false);
    };

    const selectedTypeName = 
        disasterTypes.find((t) => String(t.id) === String(selectedDisasterType))?.name || '';


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

                    <Link
                        to="/disaster-plan-generator"
                        className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                    >
                        Change Plan Type
                    </Link>
                </div>
            </nav>

            <main className="flex-grow">
                { /* Hero Band with Step Indicator */ }
                <section className="relative overflow-hidden bg-gradient-to-br from-emerald-900 via-emerald-800 to-teal-700 text-white">
                    <div className="absolute inset-0 opacity-10 [background-image:radial-gradient(circle_at_1px_1px,white_1px,transparent_0)] [background-size:24px_24px]" />
                    <div className="relative mx-auto max-w-7xl px-6 py-16 lg:px-8">
                        <ol className="flex flex-wrap items-center justify-center gap-3 text-sm">
                            {STEPS.map((label, index) => {
                                const isComplete = index < step
                                const isActive = index === step

                                return (
                                    <li key={label} className="flex items-center gap-3">
                                        <span 
                                            className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold ${
                                                isActive || isComplete
                                                ? 'bg-white text-emerald-800'
                                                : 'bg-white/10 text-emerald-100 ring-1 ring-inset ring-white/20'
                                            }`}
                                        >
                                            {isComplete ? '✓' : index + 1}
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
                                Generic Plans for: <strong>{selectedTypeName}</strong>
                            </span>
                            <h1 className="mt-6 text-4xl font-extrabold tracking-tight sm:text-5xl">
                                Disaster Plan Generator
                            </h1>
                            <p className="mt-4 text-lg leading-8 text-emerald-100">
                                Generate a disaster plan that works for any veterinary clinic
                            </p>
                        </div>
                    </div>
                </section>

                <div className="mx-auto max-w-4xl px-6 py-16 lg:px-8">
                    {error && (
                        <div className="mb-8 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                            {error}
                        </div>
                    )}

                    { /* Step 0: Select Disaster Type */ }
                    {step === 0 && (
                        <div className="rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
                            <h2 className="text-xl font-semibold text-slate-900">
                                Select a Disaster Type
                            </h2>
                            <p className="mt-2 text-sm text-slate-600">
                                Choose the hazard you want to address.
                            </p>

                            <label htmlFor="disasterType" className="mt-6 block text-sm font-medium text-slate-700">
                                Disaster Type
                            </label>
                            <select
                                id="disasterType"
                                value={selectedDisasterType}
                                onChange={(e) => setSelectedDisasterType(e.target.value)}
                                className="mt-2 block w-full rounded-md border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 shadow-sm focus:border-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-600/30"
                            >
                                <option value="">Select a disaster type</option>
                                {disasterTypes.map((type) => (
                                    <option key={type.id} value={type.id}>
                                        {type.name}
                                    </option>
                                ))}
                            </select>

                            <button
                                onClick={handleGeneratePlan}
                                disabled={!selectedDisasterType}
                                className={`mt-8 rounded-md px-6 py-3 text-sm font-semibold shadow-sm transition ${
                                    selectedDisasterType
                                        ? 'bg-emerald-700 text-white hover:bg-emerald-800'
                                        : 'cursor-not-allowed bg-slate-200 text-slate-500'
                                }`}
                            >
                                Generate Plan <span aria-hidden="true">&rarr;</span>
                            </button>
                        </div>
                    )}

                    { /* Step 1: Loading / Generating Plan */ }
                    {loading && (
                        <div className="flex flex-col items-center justify-center rounded-xl border border-slate-200 bg-white p-12 shadow-sm">
                            <span className="h-10 w-10 animate-spin rounded-full border-4 border-emerald-100 border-t-emerald-700" />
                            <p className="mt-4 text-sm text-slate-600">Generating your plan...</p>
                        </div>
                    )}

                    { /* Step 2: Review & Finalize Plan */ }
                    {plan && !editMode && step === 2 && (
                        <div className="space-y-6">
                            <div className="rounded-xl border border-emerald-200 bg-emerald-50/60 p-8">
                                <p className="text-xs font-semibold uppercase tracking-wider text-emerald-700">
                                    {selectedTypeName || 'Disaster Plan'}
                                </p>
                                <h2 className="mt-2 text-2xl font-bold text-slate-900">
                                    {plan.name || 'Generated Disaster Plan'}
                                </h2>
                                {plan.description && (
                                    <p className="mt-3 text-sm leading-6 text-slate-700">{plan.description}</p>
                                )}
                            </div>

                            {plan.common_regions?.length > 0 && (
                                <Section title="Commonly Affected Regions">
                                    <BulletList items={plan.common_regions} />
                                </Section>
                            )}

                            {plan.response_steps?.length > 0 && (
                                <Section title="Response Steps">
                                    <BulletList items={plan.response_steps} />
                                </Section>
                            )}

                            {plan.recovery_steps?.length > 0 && (
                                <Section title="Recovery Steps">
                                    <BulletList items={plan.recovery_steps} />
                                </Section>
                            )}

                            {plan.emergency_contacts?.length > 0 && (
                                <Section title="Emergency Contacts">
                                    <BulletList items={plan.emergency_contacts} 
                                        render={(contact) => (
                                        <>
                                            <strong className="font-semibold text-slate-900">{contact.name}:</strong>{' '}
                                            {contact.phone} <span className="text-slate-500">({contact.type})</span>
                                        </>
                                        )}
                                    />
                                </Section>
                            )}

                            {plan.supplies_needed?.length > 0 && (
                                <Section title="Supplies Needed">
                                    <BulletList items={plan.supplies_needed} 
                                        render={(supply) => (
                                        <>
                                            <strong className="font-semibold text-slate-900">{supply.item}:</strong>{' '}
                                            {supply.quantity} {supply.unit}
                                        </>
                                        )}
                                    />
                                </Section>
                            )}

                            {plan.training_requirements?.length > 0 && (
                                <Section title="Training Requirements">
                                    <BulletList items={plan.training_requirements} />
                                </Section>
                            )}

                            <div className="flex flex-col-reverse gap-4 border-t border-slate-200 pt-8 sm:flex-row sm:justify-between">
                                <button
                                    onClick={handleStartOver}
                                    className="rounded-md border border-slate-300 px-6 py-3 text-center text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                                >
                                    Start Over
                                </button>
                                <div className="flex flex-col gap-4 sm:flex-row">
                                    <button
                                        onClick={() => setEditMode(true)}
                                        className="rounded-md border border-emerald-700 px-6 py-3 text-center text-sm font-semibold text-emerald-700 transition hover:bg-emerald-50"
                                    >
                                        Edit Plan
                                    </button>
                                    <button
                                        onClick={handleSavePlan}
                                        className="rounded-md bg-emerald-700 px-6 py-3 text-center text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800"
                                    >
                                        Save Plan
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    { /* Edit Mode */ }
                    {editMode && plan && (
                        <div className="rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
                            <h2 className="text-xl font-semibold text-slate-900">Edit Disaster Plan</h2>
                            <p className="mt-2 text-sm text-slate-600">Update the plan text below, then save your changes.</p>

                            <textarea
                                value={plan.plan_text || ''}
                                onChange={(e) => setPlan({ ...plan, plan_text: e.target.value})}
                                className="mt-6 h-80 w-full rounded-md border border-slate-300 p-4 text-sm leading-6 text-slate-900 shadow-sm focus:border-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-600/30"
                            />

                            <div className="mt-6 flex justify-end">
                                <button
                                    onClick={handleSavePlan}
                                    className="rounded-md bg-emerald-700 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800"
                                >
                                    Save Changes
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </main>

            { /* Footer */ }
            <Footer />
        </div>
    );
}
export default GenericDisasterPlans