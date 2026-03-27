<<<<<<< C:/Users/PC DZ/Desktop/AUTO-P/frontend/src/components/pages/Modeles.jsx
import React, { useState, useEffect } from 'react'
import { Search, Filter, Car, Calendar, Fuel, Settings, Star, BarChart3, Zap, Award, Grid, List, Plus, X, Check, ChevronRight, Heart, Compare } from 'lucide-react'

export default function Modeles() {
  const [modeles, setModeles] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedMarque, setSelectedMarque] = useState('')
  const [selectedCategorie, setSelectedCategorie] = useState('')
  const [sortBy, setSortBy] = useState('popularite')
  const [viewMode, setViewMode] = useState('grid')
  const [compareMode, setCompareMode] = useState(false)
  const [selectedForCompare, setSelectedForCompare] = useState([])
  const [showCompareModal, setShowCompareModal] = useState(false)
  const [showFicheModal, setShowFicheModal] = useState(false)
  const [selectedModele, setSelectedModele] = useState(null)
  const [favorites, setFavorites] = useState([])

  useEffect(() => {
    fetchModeles()
  }, [])

  const fetchModeles = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:8000/api/modeles/')
      if (!response.ok) throw new Error('Failed to fetch modeles')
      
      const data = await response.json()
      const transformedModeles = data.map(modele => ({
        ...modele,
        fichetechnique: modele.fichetechnique || {
          dimensions: { longueur: 4.0, largeur: 1.7, hauteur: 1.5, coffre: 300 },
          performances: { 0_100: 12, vmax: 180, consommation: 5.5, co2: 120 },
          moteur: { cylindree: 1.2, puissance: 110, couple: 205, carburant: 'essence' },
          securite: { airbags: 6, abs: true, esp: true, note_euro_ncap: 5 }
        }
      }))
      setModeles(transformedModeles)
    } catch (error) {
      // Fallback données simulées
      setModeles([
        {
          id: 1, nom: '208', marque_nom: 'Peugeot', categorie: 'citadine',
          fichetechnique: {
            dimensions: { longueur: 4.0, largeur: 1.74, hauteur: 1.43, coffre: 265 },
            performances: { 0_100: 11.3, vmax: 190, consommation: 5.1, co2: 115 },
            moteur: { cylindree: 1.2, puissance: 110, couple: 205, carburant: 'essence' },
            securite: { airbags: 6, abs: true, esp: true, note_euro_ncap: 5 }
          }
        }
      ])
    } finally {
      setLoading(false)
    }
  }
          {
            id: 2,
            nom: '308',
            marque_nom: 'Peugeot',
            categorie: 'berline',
            annee_debut: 2007,
            annee_fin: null,
            nombre_annonces: 654,
            prix_moyen: 18500,
            popularite: 78,
            description: 'Berline compacte élégante avec un design sophistiqué.'
          },
          {
            id: 3,
            nom: 'Clio',
            marque_nom: 'Renault',
            categorie: 'citadine',
            annee_debut: 1990,
            annee_fin: null,
            nombre_annonces: 923,
            prix_moyen: 13800,
            popularite: 82,
            description: 'La citadine la plus vendue en France, polyvalente et économique.'
          },
          {
            id: 4,
            nom: 'Captur',
            marque_nom: 'Renault',
            categorie: 'suv',
            annee_debut: 2013,
            annee_fin: null,
            nombre_annonces: 567,
            prix_moyen: 16500,
            popularite: 75,
            description: 'SUV compact urbain avec un design moderne et habitable.'
          },
          {
            id: 5,
            nom: 'Golf',
            marque_nom: 'Volkswagen',
            categorie: 'berline',
            annee_debut: 1974,
            annee_fin: null,
            nombre_annonces: 789,
            prix_moyen: 18200,
            popularite: 90,
            description: 'La berline compacte de référence, connue pour sa qualité.'
          },
          {
            id: 6,
            nom: 'Tiguan',
            marque_nom: 'Volkswagen',
            categorie: 'suv',
            annee_debut: 2007,
            annee_fin: null,
            nombre_annonces: 432,
            prix_moyen: 21500,
            popularite: 73,
            description: 'SUV compact familial avec un habitacle spacieux et modulable.'
          },
          {
            id: 7,
            nom: 'Série 3',
            marque_nom: 'BMW',
            categorie: 'berline',
            annee_debut: 1975,
            annee_fin: null,
            nombre_annonces: 345,
            prix_moyen: 24800,
            popularite: 78,
            description: 'Berline premium sportive, référence du segment.'
          },
          {
            id: 8,
            nom: 'X1',
            marque_nom: 'BMW',
            categorie: 'suv',
            annee_debut: 2009,
            annee_fin: null,
            nombre_annonces: 234,
            prix_moyen: 26500,
            popularite: 70,
            description: 'SUV compact premium avec des performances sportives.'
          },
          {
            id: 9,
            nom: 'Yaris',
            marque_nom: 'Toyota',
            categorie: 'citadine',
            annee_debut: 1999,
            annee_fin: null,
            nombre_annonces: 456,
            prix_moyen: 14200,
            popularite: 80,
            description: 'Citadine fiable et économique, disponible en version hybride.'
          },
          {
            id: 10,
            nom: 'RAV4',
            marque_nom: 'Toyota',
            categorie: 'suv',
            annee_debut: 1994,
            annee_fin: null,
            nombre_annonces: 321,
            prix_moyen: 19800,
            popularite: 75,
            description: 'SUV compact hybride, pionnier du segment.'
          }
        ])
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching modeles:', error)
      setLoading(false)
    }
  }

  const filteredModeles = modeles.filter(modele => {
    const matchesSearch = modele.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         modele.marque_nom.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesMarque = !selectedMarque || modele.marque_nom === selectedMarque
    return matchesSearch && matchesMarque
  })

  const marquesUniques = [...new Set(modeles.map(m => m.marque_nom))]

  const getCategorieColor = (categorie) => {
    const colors = {
      'citadine': 'text-blue-500',
      'berline': 'text-green-500',
      'suv': 'text-orange-500',
      'compact': 'text-purple-500',
      'monospace': 'text-red-500',
      'coupe': 'text-yellow-500',
      'cabriolet': 'text-pink-500',
      'utilitaire': 'text-gray-500'
    }
    return colors[categorie] || 'text-gray-500'
  }

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Modèles automobiles</h1>
          <p className="text-primary-text-secondary">Explorez tous les modèles disponibles par marque et catégorie</p>
        </div>

        {/* Filtres */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary-text-secondary" />
              <input
                type="text"
                placeholder="Rechercher un modèle..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
              />
            </div>
            <div>
              <select
                value={selectedMarque}
                onChange={(e) => setSelectedMarque(e.target.value)}
                className="w-full px-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
              >
                <option value="">Toutes les marques</option>
                {marquesUniques.map(marque => (
                  <option key={marque} value={marque}>{marque}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Car className="w-8 h-8 text-accent" />
              <span className="text-2xl font-bold text-primary-text-primary">{modeles.length}</span>
            </div>
            <p className="text-primary-text-secondary">Modèles totaux</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Star className="w-8 h-8 text-accent-secondary" />
              <span className="text-2xl font-bold text-primary-text-primary">{marquesUniques.length}</span>
            </div>
            <p className="text-primary-text-secondary">Marques</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Calendar className="w-8 h-8 text-success" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {modeles.reduce((sum, modele) => sum + modele.nombre_annonces, 0).toLocaleString()}
              </span>
            </div>
            <p className="text-primary-text-secondary">Annonces totales</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Fuel className="w-8 h-8 text-warning" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {Math.round(modeles.reduce((sum, modele) => sum + modele.prix_moyen, 0) / modeles.length).toLocaleString()}€
              </span>
            </div>
            <p className="text-primary-text-secondary">Prix moyen</p>
          </div>
        </div>

        {/* Grid des modèles */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(9)].map((_, index) => (
              <div key={index} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 animate-pulse-slow">
                <div className="h-6 bg-primary-elevated rounded mb-2"></div>
                <div className="h-4 bg-primary-elevated rounded mb-4"></div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="h-4 bg-primary-elevated rounded"></div>
                  <div className="h-4 bg-primary-elevated rounded"></div>
                </div>
                <div className="h-8 bg-primary-elevated rounded"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredModeles.map((modele) => (
              <div key={modele.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 hover:shadow-card-hover transition-all duration-300">
                {/* Header modèle */}
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-primary-text-primary">{modele.nom}</h3>
                    <p className="text-sm text-primary-text-secondary">{modele.marque_nom}</p>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-warning" />
                    <span className="text-sm font-medium text-primary-text-primary">{modele.popularite}%</span>
                  </div>
                </div>
                
                {/* Badge catégorie */}
                <div className="mb-4">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getCategorieColor(modele.categorie)} bg-current bg-opacity-10`}>
                    {modele.categorie}
                  </span>
                </div>
                
                {/* Description */}
                <p className="text-primary-text-secondary text-sm mb-4 line-clamp-2">
                  {modele.description}
                </p>
                
                {/* Période de production */}
                <div className="flex items-center space-x-2 text-sm text-primary-text-secondary mb-4">
                  <Calendar className="w-4 h-4" />
                  <span>{modele.annee_debut} - {modele.annee_fin || 'Présent'}</span>
                </div>
                
                {/* Statistiques */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-primary-text-secondary">Annonces</p>
                    <p className="text-lg font-bold text-primary-text-primary">{modele.nombre_annonces}</p>
                  </div>
                  <div>
                    <p className="text-sm text-primary-text-secondary">Prix moyen</p>
                    <p className="text-lg font-bold text-accent">{modele.prix_moyen.toLocaleString()}€</p>
                  </div>
                </div>
                
                {/* Barre de popularité */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-primary-text-secondary">Popularité</span>
                    <span className="text-primary-text-primary">{modele.popularite}%</span>
                  </div>
                  <div className="w-full bg-primary-elevated rounded-lg h-2">
                    <div 
                      className="h-full bg-gradient-to-r from-accent to-accent-secondary rounded-lg"
                      style={{ width: `${modele.popularite}%` }}
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
=======
import React, { useState, useEffect } from 'react'
import { Search, Filter, Car, Calendar, Fuel, Settings, Star, BarChart3, Zap, Award, Grid, List, Plus, X, Check, ChevronRight, Heart, Compare } from 'lucide-react'

export default function Modeles() {
  const [modeles, setModeles] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedMarque, setSelectedMarque] = useState('')
  const [selectedCategorie, setSelectedCategorie] = useState('')
  const [sortBy, setSortBy] = useState('popularite')
  const [viewMode, setViewMode] = useState('grid')
  const [compareMode, setCompareMode] = useState(false)
  const [selectedForCompare, setSelectedForCompare] = useState([])
  const [showCompareModal, setShowCompareModal] = useState(false)
  const [showFicheModal, setShowFicheModal] = useState(false)
  const [selectedModele, setSelectedModele] = useState(null)
  const [favorites, setFavorites] = useState([])

  useEffect(() => {
    fetchModeles()
  }, [])

  const fetchModeles = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:8000/api/modeles/')
      if (!response.ok) throw new Error('Failed to fetch modeles')
      
      const data = await response.json()
      const transformedModeles = data.map(modele => ({
        ...modele,
        fichetechnique: modele.fichetechnique || {
          dimensions: { longueur: 4.0, largeur: 1.7, hauteur: 1.5, coffre: 300 },
          performances: { '0_100': 12, vmax: 180, consommation: 5.5, co2: 120 },
          moteur: { cylindree: 1.2, puissance: 110, couple: 205, carburant: 'essence' },
          securite: { airbags: 6, abs: true, esp: true, note_euro_ncap: 5 }
        }
      }))
      setModeles(transformedModeles)
    } catch (error) {
      // Fallback données simulées
      setModeles([
        {
          id: 1, nom: '208', marque_nom: 'Peugeot', categorie: 'citadine',
          fichetechnique: {
            dimensions: { longueur: 4.0, largeur: 1.74, hauteur: 1.43, coffre: 265 },
            performances: { '0_100': 11.3, vmax: 190, consommation: 5.1, co2: 115 },
            moteur: { cylindree: 1.2, puissance: 110, couple: 205, carburant: 'essence' },
            securite: { airbags: 6, abs: true, esp: true, note_euro_ncap: 5 }
          }
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const filteredModeles = modeles.filter(modele => {
    const matchesSearch = modele.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         modele.marque_nom.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesMarque = !selectedMarque || modele.marque_nom === selectedMarque
    return matchesSearch && matchesMarque
  })

  const marquesUniques = [...new Set(modeles.map(m => m.marque_nom))]

  const getCategorieColor = (categorie) => {
    const colors = {
      'citadine': 'text-blue-500',
      'berline': 'text-green-500',
      'suv': 'text-orange-500',
      'compact': 'text-purple-500',
      'monospace': 'text-red-500',
      'coupe': 'text-yellow-500',
      'cabriolet': 'text-pink-500',
      'utilitaire': 'text-gray-500'
    }
    return colors[categorie] || 'text-gray-500'
  }

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Modèles automobiles</h1>
          <p className="text-primary-text-secondary">Explorez tous les modèles disponibles par marque et catégorie</p>
        </div>

        {/* Filtres */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary-text-secondary" />
              <input
                type="text"
                placeholder="Rechercher un modèle..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
              />
            </div>
            <div>
              <select
                value={selectedMarque}
                onChange={(e) => setSelectedMarque(e.target.value)}
                className="w-full px-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
              >
                <option value="">Toutes les marques</option>
                {marquesUniques.map(marque => (
                  <option key={marque} value={marque}>{marque}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Car className="w-8 h-8 text-accent" />
              <span className="text-2xl font-bold text-primary-text-primary">{modeles.length}</span>
            </div>
            <p className="text-primary-text-secondary">Modèles totaux</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Star className="w-8 h-8 text-accent-secondary" />
              <span className="text-2xl font-bold text-primary-text-primary">{marquesUniques.length}</span>
            </div>
            <p className="text-primary-text-secondary">Marques</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Calendar className="w-8 h-8 text-success" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {modeles.reduce((sum, modele) => sum + modele.nombre_annonces, 0).toLocaleString()}
              </span>
            </div>
            <p className="text-primary-text-secondary">Annonces totales</p>
          </div>
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <Fuel className="w-8 h-8 text-warning" />
              <span className="text-2xl font-bold text-primary-text-primary">
                {Math.round(modeles.reduce((sum, modele) => sum + modele.prix_moyen, 0) / modeles.length).toLocaleString()}€
              </span>
            </div>
            <p className="text-primary-text-secondary">Prix moyen</p>
          </div>
        </div>

        {/* Grid des modèles */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(9)].map((_, index) => (
              <div key={index} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 animate-pulse-slow">
                <div className="h-6 bg-primary-elevated rounded mb-2"></div>
                <div className="h-4 bg-primary-elevated rounded mb-4"></div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="h-4 bg-primary-elevated rounded"></div>
                  <div className="h-4 bg-primary-elevated rounded"></div>
                </div>
                <div className="h-8 bg-primary-elevated rounded"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredModeles.map((modele) => (
              <div key={modele.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 hover:shadow-card-hover transition-all duration-300">
                {/* Header modèle */}
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-primary-text-primary">{modele.nom}</h3>
                    <p className="text-sm text-primary-text-secondary">{modele.marque_nom}</p>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-warning" />
                    <span className="text-sm font-medium text-primary-text-primary">{modele.popularite}%</span>
                  </div>
                </div>
                
                {/* Badge catégorie */}
                <div className="mb-4">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getCategorieColor(modele.categorie)} bg-current bg-opacity-10`}>
                    {modele.categorie}
                  </span>
                </div>
                
                {/* Description */}
                <p className="text-primary-text-secondary text-sm mb-4 line-clamp-2">
                  {modele.description}
                </p>
                
                {/* Période de production */}
                <div className="flex items-center space-x-2 text-sm text-primary-text-secondary mb-4">
                  <Calendar className="w-4 h-4" />
                  <span>{modele.annee_debut} - {modele.annee_fin || 'Présent'}</span>
                </div>
                
                {/* Statistiques */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-primary-text-secondary">Annonces</p>
                    <p className="text-lg font-bold text-primary-text-primary">{modele.nombre_annonces}</p>
                  </div>
                  <div>
                    <p className="text-sm text-primary-text-secondary">Prix moyen</p>
                    <p className="text-lg font-bold text-accent">{modele.prix_moyen.toLocaleString()}€</p>
                  </div>
                </div>
                
                {/* Barre de popularité */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-primary-text-secondary">Popularité</span>
                    <span className="text-primary-text-primary">{modele.popularite}%</span>
                  </div>
                  <div className="w-full bg-primary-elevated rounded-lg h-2">
                    <div 
                      className="h-full bg-gradient-to-r from-accent to-accent-secondary rounded-lg"
                      style={{ width: `${modele.popularite}%` }}
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
>>>>>>> C:/Users/PC DZ/.windsurf/worktrees/AUTO-P/AUTO-P-47e4966c/frontend/src/components/pages/Modeles.jsx
