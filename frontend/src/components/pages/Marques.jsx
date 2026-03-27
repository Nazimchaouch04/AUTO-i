import React, { useState, useEffect } from 'react'
import { Search, Filter, Star, TrendingUp, Users, Car, Globe, Award, BarChart3, PieChart, Activity, Calendar, Zap, ChevronRight, Grid, List, Heart, ExternalLink, Flag, Factory } from 'lucide-react'

export default function Marques() {
  const [marques, setMarques] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('popularite')
  const [viewMode, setViewMode] = useState('grid')
  const [selectedCountry, setSelectedCountry] = useState('')
  const [priceRange, setPriceRange] = useState({ min: '', max: '' })
  const [showFilters, setShowFilters] = useState(false)
  const [selectedMarque, setSelectedMarque] = useState(null)
  const [showMarqueDetail, setShowMarqueDetail] = useState(false)
  const [favorites, setFavorites] = useState([])
  const [globalStats, setGlobalStats] = useState(null)

  useEffect(() => {
    fetchMarques()
  }, [])

  const fetchMarques = async () => {
    setLoading(true)
    try {
      // Connexion à l'API Django
      const response = await fetch('http://127.0.0.1:8000/api/marques/')
      if (!response.ok) throw new Error('Failed to fetch marques')
      
      const data = await response.json()
      
      // Transformer les données pour correspondre au format attendu
      const transformedMarques = data.map(marque => ({
        id: marque.id,
        nom: marque.nom,
        pays_origine: marque.pays_origine || 'France',
        logo: marque.logo || '/images/logos/default.png',
        nombre_modeles: marque.nombre_modeles || 12,
        nombre_annonces: marque.nombre_annonces || Math.floor(Math.random() * 2000) + 500,
        prix_moyen: marque.prix_moyen || Math.floor(Math.random() * 20000) + 10000,
        popularite: marque.popularite || Math.floor(Math.random() * 30) + 70,
        description: marque.description || `Constructeur automobile ${marque.pays_origine || 'français'}.`,
        annee_fondation: marque.annee_fondation || 1900 + Math.floor(Math.random() * 120),
        siege_social: marque.siege_social || 'Paris',
        chiffre_affaires: marque.chiffre_affaires || Math.floor(Math.random() * 50000) + 10000,
        nombre_employes: marque.nombre_employes || Math.floor(Math.random() * 100000) + 10000,
        categories: marque.categories || ['citadine', 'compact', 'berline', 'suv'],
        modeles_populaires: marque.modeles_populaires || [],
        evolution_ventes: marque.evolution_ventes || [],
        satisfaction_client: marque.satisfaction_client || Math.floor(Math.random() * 20) + 80,
        fiabilite: marque.fiabilite || Math.floor(Math.random() * 25) + 75,
        innovation: marque.innovation || Math.floor(Math.random() * 30) + 70
      }))
      
      setMarques(transformedMarques)
      calculateGlobalStats(transformedMarques)
      
    } catch (error) {
      console.error('Error fetching marques:', error)
      // Fallback vers données simulées
      const mockData = [
        {
          id: 1,
          nom: 'Peugeot',
          pays_origine: 'France',
          logo: '/images/logos/peugeot.png',
          nombre_modeles: 15,
          nombre_annonces: 2341,
          prix_moyen: 14500,
          popularite: 85,
          description: 'Constructeur automobile français spécialisé dans les véhicules particuliers et utilitaires.',
          annee_fondation: 1810,
          siege_social: 'Paris',
          chiffre_affaires: 45000,
          nombre_employes: 180000,
          categories: ['citadine', 'compact', 'berline', 'suv', 'utilitaire'],
          modeles_populaires: ['208', '308', '2008', '3008'],
          satisfaction_client: 82,
          fiabilite: 78,
          innovation: 75
        },
        {
          id: 2,
          nom: 'Renault',
          pays_origine: 'France',
          logo: '/images/logos/renault.png',
          nombre_modeles: 18,
          nombre_annonces: 2156,
          prix_moyen: 13800,
          popularite: 82,
          description: 'Groupe automobile français qui fabrique des voitures, des véhicules utilitaires et des engins.',
          annee_fondation: 1899,
          siege_social: 'Boulogne-Billancourt',
          chiffre_affaires: 55000,
          nombre_employes: 180000,
          categories: ['citadine', 'compact', 'berline', 'suv', 'électrique'],
          modeles_populaires: ['Clio', 'Captur', 'Mégane', 'Zoe'],
          satisfaction_client: 80,
          fiabilite: 76,
          innovation: 85
        },
        {
          id: 3,
          nom: 'Volkswagen',
          pays_origine: 'Allemagne',
          logo: '/images/logos/volkswagen.png',
          nombre_modeles: 22,
          nombre_annonces: 1987,
          prix_moyen: 18200,
          popularite: 90,
          description: 'Constructeur automobile allemand, leader européen et l\'un des plus grands au monde.',
          annee_fondation: 1937,
          siege_social: 'Wolfsburg',
          chiffre_affaires: 250000,
          nombre_employes: 650000,
          categories: ['compact', 'berline', 'suv', 'utilitaire'],
          modeles_populaires: ['Golf', 'Polo', 'Tiguan', 'Passat'],
          satisfaction_client: 85,
          fiabilite: 82,
          innovation: 80
        }
      ]
      setMarques(mockData)
      calculateGlobalStats(mockData)
    } finally {
      setLoading(false)
    }
  }

  const calculateGlobalStats = (marquesData) => {
    const totalAnnonces = marquesData.reduce((sum, marque) => sum + marque.nombre_annonces, 0)
    const avgPrix = Math.round(marquesData.reduce((sum, marque) => sum + marque.prix_moyen, 0) / marquesData.length)
    const avgPopularite = Math.round(marquesData.reduce((sum, marque) => sum + marque.popularite, 0) / marquesData.length)
    const topCountries = Object.entries(
      marquesData.reduce((acc, marque) => {
        acc[marque.pays_origine] = (acc[marque.pays_origine] || 0) + 1
        return acc
      }, {})
    ).sort((a, b) => b[1] - a[1]).slice(0, 3)
    
    setGlobalStats({
      totalMarques: marquesData.length,
      totalAnnonces,
      avgPrix,
      avgPopularite,
      topCountries
    })
  }

  const filteredMarques = marques.filter(marque => {
    // Recherche textuelle
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase()
      if (!marque.nom.toLowerCase().includes(searchLower) &&
          !marque.pays_origine.toLowerCase().includes(searchLower) &&
          !marque.description.toLowerCase().includes(searchLower)) {
        return false
      }
    }
    
    // Filtre pays
    if (selectedCountry && marque.pays_origine !== selectedCountry) return false
    
    // Filtre prix
    if (priceRange.min && marque.prix_moyen < parseInt(priceRange.min)) return false
    if (priceRange.max && marque.prix_moyen > parseInt(priceRange.max)) return false
    
    return true
  })

  const sortedMarques = [...filteredMarques].sort((a, b) => {
    switch (sortBy) {
      case 'nom':
        return a.nom.localeCompare(b.nom)
      case 'annonces':
        return b.nombre_annonces - a.nombre_annonces
      case 'prix_asc':
        return a.prix_moyen - b.prix_moyen
      case 'prix_desc':
        return b.prix_moyen - a.prix_moyen
      case 'modeles':
        return b.nombre_modeles - a.nombre_modeles
      case 'fiabilite':
        return b.fiabilite - a.fiabilite
      default: // popularite
        return b.popularite - a.popularite
    }
  })

  const toggleFavorite = (marqueId) => {
    setFavorites(prev => 
      prev.includes(marqueId) 
        ? prev.filter(id => id !== marqueId)
        : [...prev, marqueId]
    )
  }

  const showMarqueDetails = (marque) => {
    setSelectedMarque(marque)
    setShowMarqueDetail(true)
  }

  const getCountries = () => {
    const countries = [...new Set(marques.map(m => m.pays_origine))].sort()
    return countries
  }

  const getTopMarques = () => {
    return sortedMarques.slice(0, 3)
  }

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header amélioré */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Marques automobiles</h1>
          <p className="text-primary-text-secondary mb-4">Découvrez toutes les marques disponibles sur AutoIntel</p>
          
          {/* Stats globales compactes */}
          {globalStats && (
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                <Car className="w-4 h-4 text-accent" />
                <span>{globalStats.totalMarques} marques</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                <Users className="w-4 h-4 text-accent-secondary" />
                <span>{globalStats.totalAnnonces.toLocaleString()} annonces</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                <TrendingUp className="w-4 h-4 text-success" />
                <span>{globalStats.avgPrix.toLocaleString()}€ avg</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                <Star className="w-4 h-4 text-warning" />
                <span>{globalStats.avgPopularite}% popularité</span>
              </div>
            </div>
          )}
        </div>

        {/* Barre de recherche et filtres avancés */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4 mb-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary-text-secondary" />
                <input
                  type="text"
                  placeholder="Rechercher une marque, un pays..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                />
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 px-6 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary hover:bg-primary-card transition-colors duration-200"
              >
                <Filter className="w-5 h-5" />
                <span>Filtres</span>
                <ChevronRight className={`w-4 h-4 transform transition-transform ${showFilters ? 'rotate-90' : ''}`} />
              </button>
              
              {/* Sélecteur de vue */}
              <div className="flex items-center border border-primary-border/DEFAULT rounded-lg">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 ${viewMode === 'grid' ? 'bg-accent text-white' : 'text-primary-text-secondary hover:bg-primary-elevated'} transition-colors duration-200`}
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 ${viewMode === 'list' ? 'bg-accent text-white' : 'text-primary-text-secondary hover:bg-primary-elevated'} transition-colors duration-200`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>
              
              {/* Tri */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
              >
                <option value="popularite">Plus populaire</option>
                <option value="annonces">Plus d'annonces</option>
                <option value="nom">Nom A-Z</option>
                <option value="prix_asc">Prix croissant</option>
                <option value="prix_desc">Prix décroissant</option>
                <option value="modeles">Plus de modèles</option>
                <option value="fiabilite">Fiabilité</option>
              </select>
            </div>
          </div>

          {/* Filtres avancés */}
          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-primary-border/DEFAULT">
              <div>
                <label className="block text-sm font-medium text-primary-text-secondary mb-2">Pays d'origine</label>
                <select
                  value={selectedCountry}
                  onChange={(e) => setSelectedCountry(e.target.value)}
                  className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
                >
                  <option value="">Tous les pays</option>
                  {getCountries().map(country => (
                    <option key={country} value={country}>{country}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-primary-text-secondary mb-2">Prix moyen minimum</label>
                <input
                  type="number"
                  value={priceRange.min}
                  onChange={(e) => setPriceRange(prev => ({ ...prev, min: e.target.value }))}
                  placeholder="0€"
                  className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-primary-text-secondary mb-2">Prix moyen maximum</label>
                <input
                  type="number"
                  value={priceRange.max}
                  onChange={(e) => setPriceRange(prev => ({ ...prev, max: e.target.value }))}
                  placeholder="50000€"
                  className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                />
              </div>
            </div>
          )}
        </div>

        {/* Statistiques globales */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Car className="w-8 h-8 text-accent" />
              <span className="text-2xl font-bold text-primary-text-primary">{marques.length}</span>
            </div>
            <p className="text-primary-text-secondary">Marques totales</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Users className="w-8 h-8 text-accent-secondary" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {marques.reduce((sum, marque) => sum + marque.nombre_annonces, 0).toLocaleString()}
              </span>
            </div>
            <p className="text-primary-text-secondary">Annonces totales</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="w-8 h-8 text-success" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {Math.round(marques.reduce((sum, marque) => sum + marque.prix_moyen, 0) / marques.length).toLocaleString()}€
              </span>
            </div>
            <p className="text-primary-text-secondary">Prix moyen</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Star className="w-8 h-8 text-warning" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {Math.round(marques.reduce((sum, marque) => sum + marque.popularite, 0) / marques.length)}%
              </span>
            </div>
            <p className="text-primary-text-secondary">Popularité moyenne</p>
          </div>
        </div>

        {/* Grid des marques */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(8)].map((_, index) => (
              <div key={index} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 animate-pulse-slow">
                <div className="h-16 bg-primary-elevated rounded-lg mb-4"></div>
                <div className="h-6 bg-primary-elevated rounded mb-2"></div>
                <div className="h-4 bg-primary-elevated rounded mb-4"></div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="h-4 bg-primary-elevated rounded"></div>
                  <div className="h-4 bg-primary-elevated rounded"></div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sortedMarques.map((marque) => (
              <div key={marque.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 hover:shadow-card-hover transition-all duration-300">
                {/* Header marque */}
                <div className="flex items-center space-x-4 mb-4">
                  <div className="w-16 h-16 bg-primary-elevated rounded-lg flex items-center justify-center">
                    <div className="text-3xl text-primary-text-secondary">🏭</div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-primary-text-primary">{marque.nom}</h3>
                    <p className="text-sm text-primary-text-secondary">{marque.pays_origine}</p>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-warning" />
                    <span className="text-sm font-medium text-primary-text-primary">{marque.popularite}%</span>
                  </div>
                </div>
                
                {/* Description */}
                <p className="text-primary-text-secondary text-sm mb-4 line-clamp-2">
                  {marque.description}
                </p>
                
                {/* Statistiques */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-primary-text-secondary">Modèles</p>
                    <p className="text-lg font-bold text-primary-text-primary">{marque.nombre_modeles}</p>
                  </div>
                  <div>
                    <p className="text-sm text-primary-text-secondary">Annonces</p>
                    <p className="text-lg font-bold text-primary-text-primary">{marque.nombre_annonces.toLocaleString()}</p>
                  </div>
                </div>
                
                {/* Prix moyen */}
                <div className="mb-4">
                  <p className="text-sm text-primary-text-secondary mb-1">Prix moyen</p>
                  <p className="text-2xl font-bold text-accent">{marque.prix_moyen.toLocaleString()}€</p>
                </div>
                
                {/* Barre de popularité */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-primary-text-secondary">Popularité</span>
                    <span className="text-primary-text-primary">{marque.popularite}%</span>
                  </div>
                  <div className="w-full bg-primary-elevated rounded-lg h-2">
                    <div 
                      className="h-full bg-gradient-to-r from-accent to-accent-secondary rounded-lg"
                      style={{ width: `${marque.popularite}%` }}
                    ></div>
                  </div>
                </div>
                
                {/* Actions */}
                <div className="flex space-x-2">
                  <button className="flex-1 bg-accent hover:bg-accent-secondary text-white py-2 rounded-lg font-medium transition-colors duration-200">
                    Voir les annonces
                  </button>
                  <button className="px-4 py-2 border border-accent text-accent hover:bg-accent hover:text-white rounded-lg font-medium transition-all duration-200">
                    <Star className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
