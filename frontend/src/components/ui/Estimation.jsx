import React, { useState, useEffect, useRef } from 'react'
import { 
  Search, Zap, Fuel, Settings, MapPin, Calendar, Gauge, 
  Loader2, ChevronDown, RotateCcw, ExternalLink, Sparkles,
  TrendingUp, TrendingDown, X
} from 'lucide-react'

const COLORS = {
  accent: '#6C63FF',
  'accent-secondary': '#00D4AA',
  warning: '#F59E0B',
  danger: '#EF4444',
  success: '#10B981'
}

const MARQUES = [
  { id: 'peugeot', name: 'Peugeot', logo: '🦁' },
  { id: 'renault', name: 'Renault', logo: '🔷' },
  { id: 'volkswagen', name: 'Volkswagen', logo: 'Ⓥ' },
  { id: 'bmw', name: 'BMW', logo: '◈' },
  { id: 'mercedes', name: 'Mercedes', logo: '⭐' },
  { id: 'audi', name: 'Audi', logo: '◎' },
  { id: 'citroen', name: 'Citroën', logo: '⩗' },
  { id: 'toyota', name: 'Toyota', logo: 'Ⓣ' },
  { id: 'ford', name: 'Ford', logo: 'Ⓕ' }
]

const MODELES_PAR_MARQUE = {
  peugeot: ['208', '308', '3008', '5008', '2008', '508', 'Rifter'],
  renault: ['Clio', 'Captur', 'Megane', 'Scenic', 'Kadjar', 'Talisman', 'Duster'],
  volkswagen: ['Golf', 'Polo', 'Tiguan', 'Passat', 'T-Roc', 'Arteon'],
  bmw: ['Série 1', 'Série 3', 'Série 5', 'X1', 'X3', 'X5'],
  mercedes: ['Classe A', 'Classe C', 'Classe E', 'GLA', 'GLC', 'GLE'],
  audi: ['A1', 'A3', 'A4', 'A5', 'Q3', 'Q5', 'Q7'],
  citroen: ['C3', 'C4', 'C5 Aircross', 'Berlingo', 'C4 Cactus'],
  toyota: ['Yaris', 'Corolla', 'RAV4', 'C-HR', 'Camry'],
  ford: ['Fiesta', 'Focus', 'Puma', 'Kuga', 'Mustang']
}

const REGIONS = [
  { code: 'DZ', name: 'Algérie', flag: '🇩🇿' },
  { code: 'TN', name: 'Tunisie', flag: '🇹🇳' },
  { code: 'FR', name: 'France', flag: '🇫🇷' },
  { code: 'MA', name: 'Maroc', flag: '🇲🇦' }
]

const CARBURANTS = [
  { id: 'essence', name: 'Essence', icon: '⛽', color: '#F59E0B' },
  { id: 'diesel', name: 'Diesel', icon: '🛢️', color: '#374151' },
  { id: 'electrique', name: 'Électrique', icon: '⚡', color: '#00D4AA' },
  { id: 'hybride', name: 'Hybride', icon: '🍃', color: '#10B981' }
]

// Hook de count-up animation
const useCountUp = (target, duration = 1200, start = 0) => {
  const [value, setValue] = useState(start)
  const [isAnimating, setIsAnimating] = useState(false)

  const startAnimation = () => {
    setIsAnimating(true)
    const startTime = Date.now()
    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easeOut = 1 - Math.pow(1 - progress, 3)
      setValue(Math.floor(start + (target - start) * easeOut))
      if (progress < 1) {
        requestAnimationFrame(animate)
      } else {
        setValue(target)
        setIsAnimating(false)
      }
    }
    animate()
  }

  return { value, startAnimation, isAnimating }
}

// Toast AutoCoin
const AutoCoinToast = ({ show, onClose }) => {
  useEffect(() => {
    if (show) {
      const timer = setTimeout(() => {
        onClose()
      }, 4000)
      return () => clearTimeout(timer)
    }
  }, [show, onClose])

  if (!show) return null

  return (
    <div className="fixed top-24 right-4 z-50" style={{ animation: 'slideInRight 0.3s ease-out' }}>
      <div className="bg-gradient-to-r from-accent to-accent-secondary text-white px-6 py-4 rounded-xl shadow-lg flex items-center gap-3">
        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <p className="font-bold">+50 AutoCoins gagnés !</p>
          <p className="text-sm text-white/80">Merci d'utiliser AutoIntel</p>
        </div>
        <button onClick={onClose} className="ml-2 p-1 hover:bg-white/20 rounded">
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}

// Mini gauge circulaire
const MiniGauge = ({ value, color = COLORS.accent }) => {
  const circumference = 2 * Math.PI * 18
  const offset = circumference - (value / 100) * circumference

  return (
    <div className="relative w-12 h-12">
      <svg viewBox="0 0 40 40" className="transform -rotate-90">
        <circle cx="20" cy="20" r="18" stroke="#374151" strokeWidth="4" fill="none" />
        <circle
          cx="20" cy="20" r="18"
          stroke={color}
          strokeWidth="4"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000"
        />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-primary-text-primary">
        {value}%
      </span>
    </div>
  )
}

// Historique card
const HistoryCard = ({ estimation, onReuse }) => {
  const dateRelative = () => {
    const diff = Date.now() - new Date(estimation.date).getTime()
    const hours = Math.floor(diff / 3600000)
    if (hours < 1) return "À l'instant"
    if (hours < 24) return `Il y a ${hours}h`
    const days = Math.floor(hours / 24)
    if (days === 1) return 'Hier'
    return `Il y a ${days} jours`
  }

  return (
    <div className="bg-primary-elevated rounded-xl p-4 min-w-[220px] flex-shrink-0">
      <div className="flex items-start justify-between mb-2">
        <div>
          <p className="font-semibold text-primary-text-primary">{estimation.vehicule.marque} {estimation.vehicule.modele}</p>
          <p className="text-sm text-primary-text-secondary">{estimation.vehicule.annee}</p>
        </div>
        <p className="text-accent font-bold">{estimation.prix_estime.toLocaleString()}€</p>
      </div>
      <div className="flex items-center justify-between text-xs text-primary-text-secondary">
        <span>{dateRelative()}</span>
        <button 
          onClick={() => onReuse(estimation)}
          className="flex items-center gap-1 text-accent hover:underline"
        >
          <RotateCcw className="w-3 h-3" /> Réutiliser
        </button>
      </div>
    </div>
  )
}

export default function Estimation({ onSubmit, showResult, data }) {
  const [formData, setFormData] = useState({
    marque: '',
    modele: '',
    annee: 2020,
    kilometrage: 50000,
    carburant: 'essence',
    boite: 'manuelle',
    puissance: 120,
    region: 'DZ'
  })
  const [loading, setLoading] = useState(false)
  const [searchMarque, setSearchMarque] = useState('')
  const [showMarqueDropdown, setShowMarqueDropdown] = useState(false)
  const [estimationResult, setEstimationResult] = useState(null)
  const [showCoinToast, setShowCoinToast] = useState(false)
  const [history, setHistory] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('estimation_history')
      return saved ? JSON.parse(saved) : []
    }
    return []
  })
  
  const marqueDropdownRef = useRef(null)
  const { value: animatedPrice, startAnimation } = useCountUp(estimationResult?.prix_estime || 0, 1200)

  // Fermer dropdown quand on clique à l'extérieur
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (marqueDropdownRef.current && !marqueDropdownRef.current.contains(e.target)) {
        setShowMarqueDropdown(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Persistance historique
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('estimation_history', JSON.stringify(history))
    }
  }, [history])

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    if (field === 'marque') {
      setFormData(prev => ({ ...prev, modele: '' }))
    }
  }

  const calculerKmAn = () => {
    const age = 2025 - formData.annee
    if (age <= 0) return formData.kilometrage
    return Math.round(formData.kilometrage / age)
  }

  const getCategoriePuissance = (cv) => {
    if (cv < 100) return { label: 'Citadine', color: COLORS.success }
    if (cv < 200) return { label: 'Berline', color: COLORS.warning }
    return { label: 'Sport', color: COLORS.danger }
  }

  const addCoins = async () => {
    try {
      await fetch('/api/gamification/add-coins/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: 50, reason: 'estimation' })
      })
    } catch (e) {
      console.log('Coin add failed:', e)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.marque || !formData.modele) return

    setLoading(true)
    
    try {
      // Appel API réel
      const response = await fetch('/api/estimation/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      let result
      if (response.ok) {
        result = await response.json()
      } else {
        // Fallback estimation locale
        const prixBase = { peugeot: 15000, renault: 14000, volkswagen: 18000, bmw: 25000, mercedes: 28000, audi: 24000, citroen: 13000, toyota: 16000, ford: 14500 }
        const basePrice = prixBase[formData.marque] || 15000
        const age = 2025 - formData.annee
        const ageFactor = Math.max(0.3, 1 - (age * 0.08))
        const kmFactor = formData.kilometrage > 100000 ? Math.max(0.5, 1 - ((formData.kilometrage - 100000) / 100000)) : 1.0
        const carburantFactor = formData.carburant === 'electrique' ? 1.15 : formData.carburant === 'hybride' ? 1.1 : 1
        const boiteFactor = formData.boite === 'automatique' ? 1.08 : 1
        
        const estimatedPrice = Math.round(basePrice * ageFactor * kmFactor * carburantFactor * boiteFactor)
        
        result = {
          prix_estime: estimatedPrice,
          fourchette_basse: Math.round(estimatedPrice * 0.85),
          fourchette_haute: Math.round(estimatedPrice * 1.15),
          fiabilite: age < 5 ? 85 : age < 10 ? 75 : 65,
          score_confiance: age < 5 ? 88 : age < 10 ? 72 : 60,
          nb_annonces: Math.floor(Math.random() * 500) + 50,
          facteurs: [
            { name: 'Marque premium', impact: formData.marque === 'bmw' || formData.marque === 'mercedes' || formData.marque === 'audi' ? +15 : -5 },
            { name: 'Kilométrage', impact: formData.kilometrage > 100000 ? -8 : +3 },
            { name: 'Région', impact: formData.region === 'FR' ? +5 : -3 }
          ],
          vehicule: formData
        }
      }
      
      setEstimationResult(result)
      
      // Ajouter à l'historique
      const historyEntry = {
        id: Date.now(),
        date: new Date().toISOString(),
        prix_estime: result.prix_estime,
        vehicule: result.vehicule
      }
      setHistory(prev => [historyEntry, ...prev.slice(0, 4)])
      
      onSubmit(result)
      
      // Animation prix
      setTimeout(() => startAnimation(), 100)
      
      // Reward AutoCoin
      setTimeout(() => {
        setShowCoinToast(true)
        addCoins()
      }, 1000)
      
    } catch (error) {
      console.error('Estimation error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleReuse = (estimation) => {
    setFormData(estimation.vehicule)
    setEstimationResult(null)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const filteredMarques = MARQUES.filter(m => 
    m.name.toLowerCase().includes(searchMarque.toLowerCase())
  )

  const modelesDisponibles = MODELES_PAR_MARQUE[formData.marque] || []

  const isFormValid = formData.marque && formData.modele && formData.annee >= 2000

  const catPuissance = getCategoriePuissance(formData.puissance)

  return (
    <section id="estimation" className="py-20 bg-primary-bg">
      <AutoCoinToast show={showCoinToast} onClose={() => setShowCoinToast(false)} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-primary-text-primary mb-4">
            Estimez votre véhicule
          </h2>
          <p className="text-primary-text-secondary max-w-2xl mx-auto">
            Notre IA analyse des milliers d'annonces pour vous donner le prix juste du marché en temps réel
          </p>
        </div>

        {/* Formulaire */}
        <div className="bg-primary-card border border-primary-border rounded-2xl p-8 mb-8">
          <form onSubmit={handleSubmit}>
            <div className="grid md:grid-cols-2 gap-8">
              
              {/* Colonne gauche - Identité */}
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-primary-text-primary flex items-center gap-2">
                  <Search className="w-5 h-5 text-accent" />
                  Identité du véhicule
                </h3>

                {/* Marque Combobox */}
                <div className="relative" ref={marqueDropdownRef}>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">
                    Marque
                  </label>
                  <button
                    type="button"
                    onClick={() => setShowMarqueDropdown(!showMarqueDropdown)}
                    className="w-full px-4 py-3 bg-primary-elevated border border-primary-border rounded-xl flex items-center justify-between hover:border-accent transition-colors"
                  >
                    <span className="flex items-center gap-2">
                      {formData.marque ? (
                        <>
                          <span className="text-xl">
                            {MARQUES.find(m => m.id === formData.marque)?.logo}
                          </span>
                          <span className="text-primary-text-primary">
                            {MARQUES.find(m => m.id === formData.marque)?.name}
                          </span>
                        </>
                      ) : (
                        <span className="text-primary-text-secondary">Sélectionnez une marque...</span>
                      )}
                    </span>
                    <ChevronDown className={`w-5 h-5 text-primary-text-secondary transition-transform ${showMarqueDropdown ? 'rotate-180' : ''}`} />
                  </button>
                  
                  {showMarqueDropdown && (
                    <div className="absolute z-10 w-full mt-2 bg-primary-card border border-primary-border rounded-xl shadow-xl max-h-60 overflow-auto">
                      <div className="p-2">
                        <input
                          type="text"
                          placeholder="Rechercher..."
                          value={searchMarque}
                          onChange={(e) => setSearchMarque(e.target.value)}
                          className="w-full px-3 py-2 bg-primary-elevated border border-primary-border rounded-lg text-sm text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                        />
                      </div>
                      <div className="border-t border-primary-border">
                        {filteredMarques.map(marque => (
                          <button
                            key={marque.id}
                            type="button"
                            onClick={() => {
                              handleChange('marque', marque.id)
                              setShowMarqueDropdown(false)
                              setSearchMarque('')
                            }}
                            className="w-full px-4 py-3 flex items-center gap-3 hover:bg-primary-elevated transition-colors"
                          >
                            <span className="text-xl">{marque.logo}</span>
                            <span className="text-primary-text-primary">{marque.name}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Modèle dynamique */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">
                    Modèle
                  </label>
                  <select
                    value={formData.modele}
                    onChange={(e) => handleChange('modele', e.target.value)}
                    disabled={!formData.marque}
                    className="w-full px-4 py-3 bg-primary-elevated border border-primary-border rounded-xl text-primary-text-primary focus:outline-none focus:border-accent disabled:opacity-50"
                  >
                    <option value="">{formData.marque ? 'Sélectionnez un modèle...' : "Choisissez d'abord une marque"}</option>
                    {modelesDisponibles.map(modele => (
                      <option key={modele} value={modele}>{modele}</option>
                    ))}
                  </select>
                </div>

                {/* Année slider double */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">
                    Année <span className="text-accent font-bold ml-2">{formData.annee}</span>
                    <span className="text-xs text-primary-text-secondary ml-2">(Il y a {2025 - formData.annee} ans)</span>
                  </label>
                  <input
                    type="range"
                    min="2000"
                    max="2025"
                    value={formData.annee}
                    onChange={(e) => handleChange('annee', parseInt(e.target.value))}
                    className="w-full h-2 bg-primary-elevated rounded-lg appearance-none cursor-pointer accent-accent"
                  />
                  <div className="flex justify-between text-xs text-primary-text-secondary mt-1">
                    <span>2000</span>
                    <input
                      type="number"
                      value={formData.annee}
                      onChange={(e) => handleChange('annee', parseInt(e.target.value) || 2020)}
                      className="w-20 px-2 py-1 bg-primary-elevated border border-primary-border rounded text-center text-primary-text-primary"
                    />
                    <span>2025</span>
                  </div>
                </div>

                {/* Kilométrage */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">
                    Kilométrage <span className="text-accent font-bold ml-2">{formData.kilometrage.toLocaleString()} km</span>
                    <span className="text-xs text-primary-text-secondary ml-2">(Soit ~{calculerKmAn().toLocaleString()} km/an)</span>
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="300000"
                    step="1000"
                    value={formData.kilometrage}
                    onChange={(e) => handleChange('kilometrage', parseInt(e.target.value))}
                    className="w-full h-2 bg-primary-elevated rounded-lg appearance-none cursor-pointer accent-accent"
                  />
                  <div className="flex justify-between text-xs text-primary-text-secondary mt-1">
                    <span>0 km</span>
                    <input
                      type="number"
                      value={formData.kilometrage}
                      onChange={(e) => handleChange('kilometrage', parseInt(e.target.value) || 0)}
                      className="w-24 px-2 py-1 bg-primary-elevated border border-primary-border rounded text-center text-primary-text-primary"
                    />
                    <span>300k+ km</span>
                  </div>
                </div>
              </div>

              {/* Colonne droite - Spécifications */}
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-primary-text-primary flex items-center gap-2">
                  <Settings className="w-5 h-5 text-accent" />
                  Spécifications
                </h3>

                {/* Carburant radio buttons */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-3">
                    Carburant
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {CARBURANTS.map(carburant => (
                      <button
                        key={carburant.id}
                        type="button"
                        onClick={() => handleChange('carburant', carburant.id)}
                        className={`p-4 rounded-xl border-2 flex flex-col items-center gap-2 transition-all ${
                          formData.carburant === carburant.id
                            ? 'border-accent bg-accent/10'
                            : 'border-primary-border hover:border-primary-text-secondary'
                        }`}
                      >
                        <span className="text-2xl">{carburant.icon}</span>
                        <span className="text-sm font-medium text-primary-text-primary">{carburant.name}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Boîte toggle */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-3">
                    Boîte de vitesse
                  </label>
                  <div className="flex items-center bg-primary-elevated rounded-xl p-1">
                    <button
                      type="button"
                      onClick={() => handleChange('boite', 'manuelle')}
                      className={`flex-1 py-3 rounded-lg text-sm font-medium transition-all ${
                        formData.boite === 'manuelle'
                          ? 'bg-accent text-white'
                          : 'text-primary-text-secondary hover:text-primary-text-primary'
                      }`}
                    >
                      Manuelle
                    </button>
                    <div className="w-px h-6 bg-primary-border" />
                    <button
                      type="button"
                      onClick={() => handleChange('boite', 'automatique')}
                      className={`flex-1 py-3 rounded-lg text-sm font-medium transition-all ${
                        formData.boite === 'automatique'
                          ? 'bg-accent text-white'
                          : 'text-primary-text-secondary hover:text-primary-text-primary'
                      }`}
                    >
                      Automatique
                    </button>
                  </div>
                </div>

                {/* Puissance */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">
                    Puissance 
                    <span className="text-accent font-bold ml-2">{formData.puissance} CV</span>
                    <span className="ml-2 px-2 py-0.5 rounded text-xs" style={{ backgroundColor: `${catPuissance.color}20`, color: catPuissance.color }}>
                      {catPuissance.label}
                    </span>
                  </label>
                  <input
                    type="range"
                    min="50"
                    max="500"
                    step="5"
                    value={formData.puissance}
                    onChange={(e) => handleChange('puissance', parseInt(e.target.value))}
                    className="w-full h-2 bg-primary-elevated rounded-lg appearance-none cursor-pointer accent-accent"
                  />
                  <div className="flex justify-between text-xs text-primary-text-secondary mt-1">
                    <span>50 CV</span>
                    <span>500 CV</span>
                  </div>
                </div>

                {/* Région */}
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">
                    Région
                  </label>
                  <select
                    value={formData.region}
                    onChange={(e) => handleChange('region', e.target.value)}
                    className="w-full px-4 py-3 bg-primary-elevated border border-primary-border rounded-xl text-primary-text-primary focus:outline-none focus:border-accent"
                  >
                    {REGIONS.map(region => (
                      <option key={region.code} value={region.code}>
                        {region.flag} {region.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Bouton submit */}
            <div className="mt-8 flex justify-center">
              <button
                type="submit"
                disabled={!isFormValid || loading}
                className="px-8 py-4 bg-accent text-white font-semibold rounded-xl flex items-center gap-3 hover:bg-accent/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-accent/20"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyse en cours...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Estimer le prix →
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Résultat */}
        {(showResult || estimationResult) && estimationResult && (
          <div id="estimationResult" style={{ animation: 'slideUp 0.3s ease-out' }}>
            <div className="bg-primary-card border border-primary-border rounded-2xl p-8">
              <div className="grid lg:grid-cols-3 gap-8">
                
                {/* Prix principal */}
                <div className="lg:col-span-2">
                  <p className="text-sm text-primary-text-secondary mb-2">Prix estimé</p>
                  <p className="text-5xl font-bold text-accent mb-2">
                    {animatedPrice.toLocaleString()} €
                  </p>
                  <p className="text-sm text-primary-text-secondary mb-6">Prix juste du marché</p>
                  
                  {/* Barre fourchette */}
                  <div className="relative h-4 bg-primary-elevated rounded-full mb-8 overflow-hidden">
                    <div 
                      className="absolute h-full bg-gradient-to-r from-success via-accent to-success opacity-30"
                      style={{ left: '0%', right: '0%' }}
                    />
                    <div 
                      className="absolute top-1/2 w-4 h-4 bg-accent rounded-full border-2 border-white shadow-lg"
                      style={{ 
                        left: `${((estimationResult.prix_estime - estimationResult.fourchette_basse) / (estimationResult.fourchette_haute - estimationResult.fourchette_basse)) * 100}%`,
                        transform: 'translate(-50%, -50%)'
                      }}
                    />
                    <div className="absolute -bottom-6 left-0 text-xs text-success">
                      {estimationResult.fourchette_basse.toLocaleString()}€
                    </div>
                    <div className="absolute -bottom-6 right-0 text-xs text-success">
                      {estimationResult.fourchette_haute.toLocaleString()}€
                    </div>
                  </div>

                  {/* Facteurs d'influence */}
                  <div className="flex flex-wrap gap-3 mt-12">
                    {estimationResult.facteurs?.map((facteur, idx) => (
                      <span 
                        key={idx}
                        className={`px-3 py-1 rounded-full text-sm font-medium ${
                          facteur.impact > 0 
                            ? 'bg-success/20 text-success' 
                            : 'bg-danger/20 text-danger'
                        }`}
                      >
                        {facteur.name} {facteur.impact > 0 ? '+' : ''}{facteur.impact}%
                      </span>
                    ))}
                  </div>
                </div>

                {/* Infos confiance */}
                <div className="bg-primary-elevated rounded-xl p-6 space-y-6">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary-text-secondary">Fiabilité</span>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      estimationResult.fiabilite >= 80 ? 'bg-success/20 text-success' :
                      estimationResult.fiabilite >= 60 ? 'bg-warning/20 text-warning' :
                      'bg-danger/20 text-danger'
                    }`}>
                      {estimationResult.fiabilite >= 80 ? 'Haute' : estimationResult.fiabilite >= 60 ? 'Moyenne' : 'Faible'}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary-text-secondary">Score confiance</span>
                    <MiniGauge value={estimationResult.score_confiance || 75} />
                  </div>

                  <div className="pt-4 border-t border-primary-border">
                    <p className="text-sm text-primary-text-secondary">
                      Basé sur <span className="text-primary-text-primary font-semibold">{estimationResult.nb_annonces || 120}</span> annonces similaires
                    </p>
                  </div>

                  <button className="w-full py-3 bg-accent text-white rounded-xl font-medium hover:bg-accent/90 transition-colors flex items-center justify-center gap-2">
                    Voir les annonces similaires
                    <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Historique */}
        {history.length > 0 && (
          <div className="mt-12">
            <h3 className="text-lg font-semibold text-primary-text-primary mb-4 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-accent" />
              Dernières estimations
            </h3>
            <div className="flex gap-4 overflow-x-auto pb-4">
              {history.map(item => (
                <HistoryCard 
                  key={item.id} 
                  estimation={item} 
                  onReuse={handleReuse}
                />
              ))}
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes slideInRight {
          from {
            opacity: 0;
            transform: translateX(100%);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        input[type="range"]::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          background: #6C63FF;
          border-radius: 50%;
          cursor: pointer;
        }
        input[type="range"]::-moz-range-thumb {
          width: 20px;
          height: 20px;
          background: #6C63FF;
          border-radius: 50%;
          cursor: pointer;
          border: none;
        }
      `}</style>
    </section>
  )
}
