	import { Link } from 'react-router-dom'

	function Home() {

	return (
	<>
		<nav>
			<a href=''>How It Works</a>
			<a href=''>Resources</a>
			<a href=''>Contact Us</a>
		</nav>
		<header>
            <button>ClimaVet</button>
            <button>
                <Link to="/About">Learn more</Link>
            </button>
		</header>
		<div>
            <h1>Make your clinic climate resilient</h1>
            <p>Tools and resources to help veterinary clinics prepare for climate-related disasters</p>
            <button>Get Started</button>
		</div>
		<div>
            <ul>
                <li>For Veterinarians</li>
                <li>For Clinics</li>
                <li>For Communities</li>
            </ul>
		</div>
		<div>
            <div><p>Choose a tool</p></div>
            <div>
                <button>
                    <Link to="/risk-assessment-wizard">Risk Assessment Wizard</Link>
                </button>
                <button>
                    <Link to="/disaster-plan-generator">Disaster Plan Generator</Link>
                </button>
                <button>
                    <Link to="/resource-checklist-builder">Resource Checklist Builder</Link>
                </button>
            </div>
		</div>
		<div>
            <h2>Why choose ClimaVet?</h2>
            <p>Our platform provides specialized tools and resources tailored specifically for veterinary clinics to enhance their climate resilience and preparedness.</p>
        </div>
        <footer>
            <p>ClimaVet © 2026</p>
            <p>Privacy Policy</p>
		</footer>
	</>
	)
	}

	export default Home
