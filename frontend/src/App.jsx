import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/ui/Header'
import Hero from './components/ui/Hero'
import Features from './components/ui/Features'
import Estimation from './components/ui/Estimation'
import MarketDashboard from './components/ui/Dashboard'
import Footer from './components/ui/Footer'
import Annonces from './components/pages/Annonces'
import AnnonceDetail from './components/pages/AnnonceDetail'
import Marques from './components/pages/Marques'
import Modeles from './components/pages/Modeles'
import UserDashboard from './components/pages/Dashboard'
import Profil from './components/pages/Profil'
import Alertes from './components/pages/Alertes'
import Statistiques from './components/pages/Statistiques'
import Admin from './components/pages/Admin'
import LoadingSpinner from './components/ui/LoadingSpinner'
import PrivateRoute from './components/auth/PrivateRoute'
import Login from './components/pages/auth/Login'
import Register from './components/pages/auth/Register'
import Pricing from './components/pages/Pricing'
import Boutique from './components/pages/Boutique'
import Battle from './components/pages/Battle'
import Comparison from './components/pages/Comparison'
import Battles from './components/pages/Battles'

import { useDispatch, useSelector } from 'react-redux'
import { fetchProfile } from './store/userSlice'

function App() {
  const dispatch = useDispatch()
  const { accessToken, isAuthenticated } = useSelector((state) => state.user)
  const [showEstimationResult, setShowEstimationResult] = useState(false)
  const [estimationData, setEstimationData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [darkMode, setDarkMode] = useState(true)

  // Fetch profile on mount if token exists
  useEffect(() => {
    if (accessToken && isAuthenticated) {
      dispatch(fetchProfile())
    }
  }, [dispatch, accessToken, isAuthenticated])

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
              <MarketDashboard />
              <Footer />
            </>
          } />
          
          {/* Authentification */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Pages principales publiques */}
          <Route path="/annonces" element={<Annonces />} />
          <Route path="/annonce/:id" element={<AnnonceDetail />} />
          <Route path="/marques" element={<Marques />} />
          <Route path="/modeles" element={<Modeles />} />
          <Route path="/estimation" element={<Estimation onSubmit={handleEstimationSubmit} />} />
          <Route path="/statistiques" element={<Statistiques />} />
          <Route path="/pricing" element={<Pricing />} />
          
          {/* Pages privées */}
          <Route path="/dashboard" element={<PrivateRoute><UserDashboard /></PrivateRoute>} />
          <Route path="/profil" element={<PrivateRoute><UserDashboard /></PrivateRoute>} />
          <Route path="/alertes" element={<PrivateRoute><Alertes /></PrivateRoute>} />
          <Route path="/shop" element={<PrivateRoute><Boutique /></PrivateRoute>} />
          <Route path="/battle/:id" element={<PrivateRoute><Battle /></PrivateRoute>} />
          <Route path="/compare" element={<PrivateRoute><Comparison /></PrivateRoute>} />
          <Route path="/battles" element={<PrivateRoute><Battles /></PrivateRoute>} />
          
          {/* Administration */}
          <Route path="/admin" element={<PrivateRoute><Admin /></PrivateRoute>} />
          
          {/* Redirection */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
