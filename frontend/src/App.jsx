import React, { useState, useEffect, lazy, Suspense } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { fetchProfile } from './store/userSlice'
import { ToastProvider } from './components/ui/Toast'
import LoadingScreen from './components/ui/LoadingScreen'
import { AnimatePresence } from 'framer-motion'
import MainLayout from './components/layout/MainLayout'
import PrivateRoute from './components/auth/PrivateRoute'

// --- Lazy Load Pages ---
const Hero      = lazy(() => import('./components/ui/Hero'))
const Features  = lazy(() => import('./components/ui/Features'))
const Estimation = lazy(() => import('./components/ui/Estimation'))
const MarketDashboard = lazy(() => import('./components/ui/Dashboard'))
const Footer    = lazy(() => import('./components/ui/Footer'))

const Login     = lazy(() => import('./components/pages/auth/Login'))
const Register  = lazy(() => import('./components/pages/auth/Register'))
const Annonces  = lazy(() => import('./components/pages/Annonces'))
const AnnonceDetail = lazy(() => import('./components/pages/AnnonceDetail'))
const Marques   = lazy(() => import('./components/pages/Marques'))
const Modeles   = lazy(() => import('./components/pages/Modeles'))
const UserDashboard = lazy(() => import('./components/pages/Dashboard'))
const Alertes   = lazy(() => import('./components/pages/Alertes'))
const Statistiques = lazy(() => import('./components/pages/Statistiques'))
const Admin     = lazy(() => import('./components/pages/Admin'))
const Pricing   = lazy(() => import('./components/pages/Pricing'))
const Boutique  = lazy(() => import('./components/pages/Boutique'))
const Battle    = lazy(() => import('./components/pages/Battle'))
const Comparison = lazy(() => import('./components/pages/Comparison'))
const Battles    = lazy(() => import('./components/pages/Battles'))
const AbonnementSucces = lazy(() => import('./components/pages/AbonnementSucces'))
const Assistant = lazy(() => import('./components/pages/AssistantPage'))
const Rapports = lazy(() => import('./components/pages/RapportsPage'))

function App() {
  const dispatch = useDispatch()
  const { accessToken, isAuthenticated } = useSelector((state) => state.user)
  const [showEstimationResult, setShowEstimationResult] = useState(false)
  const [estimationData, setEstimationData] = useState(null)
  const [darkMode, setDarkMode] = useState(true)

  useEffect(() => {
    if (accessToken && isAuthenticated) {
      dispatch(fetchProfile())
    }
  }, [dispatch, accessToken, isAuthenticated])

  const handleEstimationSubmit = (data) => {
    setEstimationData(data)
    setShowEstimationResult(true)
    setTimeout(() => {
      const resultElement = document.getElementById('estimationResult')
      if (resultElement) resultElement.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }

  return (
    <ToastProvider>
      <Router>
        <MainLayout darkMode={darkMode} setDarkMode={setDarkMode}>
          <Suspense fallback={<LoadingScreen />}>
            <AnimatePresence mode="wait">
              <Routes>
                {/* Home */}
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
                
                {/* Auth */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Public Pages */}
                <Route path="/annonces" element={<Annonces />} />
                <Route path="/annonce/:id" element={<AnnonceDetail />} />
                <Route path="/marques" element={<Marques />} />
                <Route path="/modeles" element={<Modeles />} />
                <Route path="/estimation" element={<Estimation onSubmit={handleEstimationSubmit} />} />
                <Route path="/statistiques" element={<Statistiques />} />
                <Route path="/pricing" element={<Pricing />} />
                <Route path="/assistant" element={<PrivateRoute><Assistant /></PrivateRoute>} />
                <Route path="/rapports" element={<PrivateRoute><Rapports /></PrivateRoute>} />
                <Route path="/abonnement/succes" element={<PrivateRoute><AbonnementSucces /></PrivateRoute>} />
                
                {/* Private Pages */}
                <Route path="/dashboard" element={<PrivateRoute><UserDashboard /></PrivateRoute>} />
                <Route path="/profil" element={<PrivateRoute><UserDashboard /></PrivateRoute>} />
                <Route path="/alertes" element={<PrivateRoute><Alertes /></PrivateRoute>} />
                <Route path="/shop" element={<PrivateRoute><Boutique /></PrivateRoute>} />
                <Route path="/battle/:id" element={<PrivateRoute><Battle /></PrivateRoute>} />
                <Route path="/compare" element={<PrivateRoute><Comparison /></PrivateRoute>} />
                <Route path="/battles" element={<PrivateRoute><Battles /></PrivateRoute>} />
                
                {/* Admin */}
                <Route path="/admin" element={<PrivateRoute><Admin /></PrivateRoute>} />
                
                {/* Redirection */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AnimatePresence>
          </Suspense>
        </MainLayout>
      </Router>
    </ToastProvider>
  )
}

export default App
