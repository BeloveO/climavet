import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/home.jsx'
import Raw from './pages/raw.jsx'
import Dpg from './pages/dpg.jsx'
import Rcb from './pages/rcg.jsx'
import About from './pages/about.jsx'
import { DisasterPlanGenerator } from './features/disasterplans/DisasterPlanGenerator.jsx'
import GenericDisasterPlans from './features/disasterplans/GenericDisasterPlanGenerator.jsx'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/risk-assessment-wizard" element={<Raw />} />
        <Route path="/disaster-plan-generator" element={<Dpg />} />
        <Route path="/resource-checklist-builder" element={<Rcb />} />
        <Route path="/custom-disaster-plans" element={<DisasterPlanGenerator />} />
        <Route path="/generic-disaster-plans" element={<GenericDisasterPlans />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
