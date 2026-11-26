	import { Link } from 'react-router-dom'
    import Navigation from './navigation'
    import Footer from './footer'

	function Home() {

        const audiences = [
            {
                title: 'For Veterinarians',
                description: 'Access specialized tools and resources to enhance your climate resilience and preparedness.',
                link: '/veterinarians'
            },
            {
                title: 'For Clinics',
                description: 'Discover tailored solutions to help your clinic prepare for climate-related disasters.',
                link: '/clinics'
            },
            {
                title: 'For Communities',
                description: 'Learn how to support your community in building climate resilience and preparedness.',
                link: '/communities'
            }
        ]

        const tools = [
            {
                title: 'Risk Assessment Wizard',
                description: 'Evaluate your clinic\'s climate resilience and identify areas for improvement.',
                link: '/risk-assessment-wizard'
            },
            {
                title: 'Disaster Plan Generator',
                description: 'Create a comprehensive disaster plan tailored to your clinic\'s needs.',
                link: '/disaster-plan-generator'
            },
            {
                title: 'Resource Checklist Builder',
                description: 'Build a customized checklist of essential resources for climate-related disasters.',
                link: '/resource-checklist-builder'
            }
        ]   

	return (
        <div className="min-h-screen flex flex-col bg-white text-slate-900 font-sans">
            {/* Navigation */}
            <Navigation />
            <main className="flex-1">
                {/* Hero Section */}
                <section className="relative overflow-hidden bg-linear-to-br from-emerald-900 via-emerald-800 to-teal-700 text-white">
                    <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_1px_1px,white_1px,transparent_0)] bg-size-[24px_24px]" />
                    <div className="relative mx-auto max-w-7xl px-6 py-24 lg:px-8 lg:py-32">
                        <div className="max-w-3xl">
                            <span className="inline-flex items-center rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-emerald-100 ring-1 ring-inset ring-white/20">
                                Climate Resilience for Veterinary Care
                            </span>
                            <h1 className="mt-6 text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
                                Empowering Veterinary Clinics to Prepare for Climate-Related Disasters
                            </h1>
                            <p className="mt-6 max-w-2xl text-lg leading-8 text-emerald-100">
                                Discover how ClimaVet helps veterinary professionals build resilience against the growing challenges of climate change.
                                Tools, resources and guidance to help your clinic prepare for climate-related disasters and ensure the safety of your patients and staff, and keep operating when it matters most
                            </p>
                            <div className="mt-10 flex flex-col gap-4 sm:flex-row">
                                <Link
                                    to="/get-started"
                                    className="rounded-md bg-white px-6 py-3 text-center text-base font-semibold text-emerald-900 shadow-lg transition hover:bg-emerald-50"
                                    >
                                    Get Started
                                </Link>
                                <Link 
                                    to="/about"
                                    className="rounded-md border border-white/30 px-6 py-3 text-center text-base font-semibold text-white transition hover:bg-white/10"
                                >
                                    Learn More
                                </Link>
                            </div>
                        </div>
                    </div>
                </section>

                { /* Audience */ }
                <section id="how-it-works" className="border-b border-slate-200 bg-slate-50">
                    <div className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
                        <ul className="grid gap-6 md:grid-cols-3">
                            {audiences.map((item) => (
                                <li 
                                    key={item.title} 
                                    className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
                                >
                                    <h3 className="text-lg font-semibold text-slate-900">{item.title}</h3>
                                    <p className="mt-2 text-sm leading-6 text-slate-600">{item.description}</p>
                                </li>
                            ))}
                        </ul>
                    </div>
                </section>

                { /* Tools */ }
                <section id="resources" className="mx-auto max-w-7xl px-6 py-20 lg:px-8">
                    <div className="max-w-2xl">
                        <h2 className="text-sm font-semibold uppercase tracking-wider text-emerald-700">Tools</h2>
                        <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                            Choose A Tool to Get Started
                        </p>
                    </div>
                    <div className="mt-12 grid gap-8 md:grid-cols-3">
                        {tools.map((tool) => (
                            <Link 
                                key={tool.link}
                                to={tool.link}
                                className="group flex flex-col rounded-xl border border-slate-200 bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:border-emerald-600 hover:shadow-lg"
                            >
                                <h3 className="text-xl font-semibold text-slate-900 group-hover:text-emerald-700">
                                    {tool.title}
                                </h3>
                                <p className="mt-3 flex-1 text-sm leading-6 text-slate-600">
                                    {tool.description}
                                </p>
                                <span className="mt-6 text-sm font-semibold text-emerald-700">
                                    Open Tool <span aria-hidden="true">&rarr;</span>
                                </span>
                            </Link>
                        ))}
                    </div>
                </section>

                { /* Value */ }
                <section id="contact" className="bg-slate-900 text-white">
                    <div className="mx-auto grid max-w-7xl gap-12 px-6 py-20 lg:grid-cols-2 lg:px-8">
                        <div>
                            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Why Choose ClimaVet?</h2>
                            <p className="mt-6 text-lg leading-8 text-slate-300">
                                The ClimaVet platform provides cutting-edge solutions and specialized tools and resources tailored specifically for the veterinary industry, helping you deliver better care to your animals.
                            </p>
                            <Link
                                to="/contact"
                                className="mt-8 inline-flex rounded-md bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:bg-emerald-400"
                            >
                                Learn More About ClimaVet
                            </Link>
                        </div>
                        <dl className="grid grid-cols-2 gap-8">
                            <div className="rounded-xl bg-white/5 p-6 ring-1 ring-white/10">
                                <dt className="text-sm text-slate-400">Tools Available</dt>
                                <dd className="mt-2 text-3xl font-bold">3</dd>
                            </div>
                            <div className="rounded-xl bg-white/5 p-6 ring-1 ring-white/10">
                                <dt className="text-sm text-slate-400">Built For</dt>
                                <dd className="mt-2 text-3xl font-bold">Veterinary Clinics</dd>
                            </div>
                        </dl>
                    </div>
                </section>
            </main>

            { /* Footer */ }
            <Footer />
        </div>
	)
	}

	export default Home
