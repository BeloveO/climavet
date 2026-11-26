import { Link } from 'react-router-dom'

function Footer() {

    return (
        <footer className="border-t border-slate-200 bg-white">
            <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-8 text-sm text-slate-500 md:flex-row lg:px-8">
                <p>&copy; 2026 ClimaVet. All rights reserved.</p>
                <Link
                    to="/privacy-policy"
                    className="font-medium text-slate-600 transition hover:text-emerald-700"
                >
                    Privacy Policy
                </Link>
            </div>
        </footer>
    )
}

export default Footer