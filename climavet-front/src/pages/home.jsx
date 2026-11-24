	import { Link } from 'react-router-dom'

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
	<>
        <div className="min-h-screen flex flex-col bg-white text-slate-900 font-sans">
            {/* Navigation */}
            <nav className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur">
                <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">
                    <Link to="/" className="flex items-center gap-2">
                        <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-700 text-lg font-bold text-white">
                            C
                        </span>
                        <span className="text-xl font-bold tracking-tight text-slate-900">ClimaVet</span>
                    </Link>

                    <div className="hidden items-center gap-8 md:flex">
                        <a href="#how-it-works" className="text-sm font-medium text-slate-600 transition hover:text-emerald-700">
                            How It Works
                        </a>
                        <a href="#resources" className="text-sm font-medium text-slate-600 transition hover:text-emerald-700">
                            Resources
                        </a>
                        <a href="#contact" className="text-sm font-medium text-slate-600 transition hover:text-emerald-700">
                            Contact Us
                        </a>
                    </div>
                    <Link
                        to="/get-started"
                        className="rounded-md bg-emerald-700 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800"
                    >
                        Get Started
                    </Link>
                </div>
            </nav>
        </div>
		
        <main className="flex-1">
            {/* Hero Section */}
        </main>
		
	</>
	)
	}

	export default Home
