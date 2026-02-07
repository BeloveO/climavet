import './App.css'
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom'
import Home from './pages/home.jsx'
import Raw from './pages/raw.jsx'
import Dpg from './pages/dpg.jsx'
import Rcb from './pages/rcg.jsx'
import About from './pages/about.jsx'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/risk-assessment-wizard" element={<Raw />} />
        <Route path="/disaster-plan-generator" element={<Dpg />} />
        <Route path="/resource-checklist-builder" element={<Rcb />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
