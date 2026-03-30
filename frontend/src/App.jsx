import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/ui/Header'
import Hero from './components/ui/Hero'
import Features from './components/ui/Features'
import Estimation from './components/ui/Estimation'
import Dashboard from './components/ui/Dashboard'
import Footer from './components/ui/Footer'
import Annonces from './components/pages/Annonces'
import AnnonceDetail from './components/pages/AnnonceDetail'
import Marques from './components/pages/Marques'
import Modeles from './components/pages/Modeles'
import Profil from './components/pages/Profil'
import Alertes from './components/pages/Alertes'
import Statistiques from './components/pages/Statistiques'
import Admin from './components/pages/Admin'
import LoadingSpinner from './components/ui/LoadingSpinner'

function App() {
  const [showEstimationResult, setShowEstimationResult] = useState(false)
  const [estimationData, setEstimationData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [darkMode, setDarkMode] = useState(true)

  // Smooth scrolling
  useEffect(() => {
    const handleSmoothScroll = (e) => {
      e.preventDefault()
      const target = document.querySelector(e.target.getAttribute('href'))
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' })
      }
    }

    const anchors = document.querySelectorAll('a[href^="#"]')
    anchors.forEach(anchor => {
      anchor.addEventListener('click', handleSmoothScroll)
    })

    return () => {
      anchors.forEach(anchor => {
        anchor.removeEventListener('click', handleSmoothScroll)
      })
    }
  }, [])

  // Handle estimation form submission
  const handleEstimationSubmit = (data) => {
    setEstimationData(data)
    setShowEstimationResult(true)
    // Scroll to result
    setTimeout(() => {
      const resultElement = document.getElementById('estimationResult')
      if (resultElement) {
        resultElement.scrollIntoView({ behavior: 'smooth' })
      }
    }, 100)
  }

  return (
    <Router>
      <div className={`min-h-screen ${darkMode ? 'bg-primary-bg' : 'bg-gray-50'}`}>
        <Header darkMode={darkMode} setDarkMode={setDarkMode} />
        
        {loading && <LoadingSpinner />}
        
        <Routes>
          {/* Page d'accueil */}
          <Route path="/" element={
            <>
              <Hero />
              <Features />
              <Estimation 
                onSubmit={handleEstimationSubmit}
                showResult={showEstimationResult}
                data={estimationData}
              />
              <Dashboard />
              <Footer />
            </>
          } />
          
          {/* Pages principales */}
          <Route path="/annonces" element={<Annonces />} />
          <Route path="/annonce/:id" element={<AnnonceDetail />} />
          <Route path="/marques" element={<Marques />} />
          <Route path="/modeles" element={<Modeles />} />
          <Route path="/estimation" element={<Estimation onSubmit={handleEstimationSubmit} />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profil" element={<Profil />} />
          <Route path="/alertes" element={<Alertes />} />
          <Route path="/statistiques" element={<Statistiques />} />
          
          {/* Administration */}
          <Route path="/admin" element={<Admin />} />
          
          {/* Redirection */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
