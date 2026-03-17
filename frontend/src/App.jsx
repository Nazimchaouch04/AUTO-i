import React from 'react'
import Header from './components/ui/Header'
import Hero from './components/ui/Hero'
import Features from './components/ui/Features'
import Estimation from './components/ui/Estimation'
import Dashboard from './components/ui/Dashboard'
import Footer from './components/ui/Footer'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Hero />
      <Features />
      <Estimation />
      <Dashboard />
      <Footer />
    </div>
  )
}

export default App
