import { Link } from 'react-router-dom';

function Navigation() {

    return (
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
    );
}

export default Navigation;