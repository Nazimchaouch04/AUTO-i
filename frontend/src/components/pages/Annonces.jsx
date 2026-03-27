import React, { useState, useEffect } from 'react'
import { Search, Filter, ChevronDown, Heart, Eye, MapPin, Calendar, Fuel, Settings, Grid, List, SlidersHorizontal, X, Check, Star, Clock, TrendingUp, Car } from 'lucide-react'

export default function Annonces() {
  const [annonces, setAnnonces] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('date_publication')
  const [viewMode, setViewMode] = useState('grid')
  const [favorites, setFavorites] = useState([])
  const [pagination, setPagination] = useState({ page: 1, limit: 12, total: 0 })
  const [filters, setFilters] = useState({
    marque: '',
    modele: '',
    prix_min: '',
    prix_max: '',
    km_max: '',
    annee_min: '',
    annee_max: '',
    carburant: '',
    boite_vitesse: '',
    categorie: '',
    departement: '',
    puissance_min: '',
    puissance_max: '',
    couleur: '',
    critair: '',
    garantie: false,
    controle_technique: false,
    premiere_main: false,
    non_fumeur: false
  })
  const [showFilters, setShowFilters] = useState(false)
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)
  const [selectedAnnonces, setSelectedAnnonces] = useState([])

  useEffect(() => {
    fetchAnnonces()
  }, [])

  const fetchAnnonces = async () => {
    setLoading(true)
    try {
      // Connexion à l'API Django
      const response = await fetch('http://127.0.0.1:8000/api/annonces/')
      if (!response.ok) throw new Error('Failed to fetch annonces')
      
      const data = await response.json()
      
      // Transformer les données pour correspondre au format attendu
      const transformedAnnonces = data.map(annonce => ({
        id: annonce.id,
        titre: annonce.titre,
        prix: annonce.prix,
        prix_estime: annonce.prix_estime || Math.round(annonce.prix * 1.15),
        kilometrage: annonce.kilometrage,
        annee: annonce.annee,
        carburant: annonce.carburant,
        boite_vitesse: annonce.boite_vitesse,
        marque_nom: annonce.marque_nom || 'Peugeot',
        modele_nom: annonce.modele_nom || '208',
        ville: annonce.ville || 'Paris',
        departement: annonce.departement || '75',
        images: annonce.images || ['/images/peugeot208-1.jpg'],
        est_bonne_affaire: annonce.est_bonne_affaire || false,
        pourcentage_economie: annonce.pourcentage_economie || 0,
        date_publication: annonce.date_publication || '2024-01-15',
        categorie: annonce.categorie || 'citadine',
        puissance: annonce.puissance || 130,
        couleur: annonce.couleur || 'Noir',
        description: annonce.description || '',
        vue_count: annonce.vue_count || Math.floor(Math.random() * 1000)
      }))
      
      setAnnonces(transformedAnnonces)
      setPagination(prev => ({ ...prev, total: transformedAnnonces.length }))
    } catch (error) {
      console.error('Error fetching annonces:', error)
      // Fallback vers données simulées
      const mockData = [
        {
          id: 1,
          titre: 'Peugeot 208 GT Line 2021',
          prix: 18500,
          prix_estime: 22000,
          kilometrage: 25000,
          annee: 2021,
          carburant: 'essence',
          boite_vitesse: 'manuelle',
          marque_nom: 'Peugeot',
          modele_nom: '208',
          ville: 'Paris',
          departement: '75',
          images: ['/images/peugeot208-1.jpg'],
          est_bonne_affaire: true,
          pourcentage_economie: 19,
          date_publication: '2024-01-15',
          categorie: 'citadine',
          puissance: 130,
          couleur: 'Noir',
          description: 'Magnifique Peugeot 208 GT Line',
          vue_count: 1234
        },
        {
          id: 2,
          titre: 'BMW Série 3 2020',
          prix: 28900,
          prix_estime: 31500,
          kilometrage: 45000,
          annee: 2020,
          carburant: 'diesel',
          boite_vitesse: 'automatique',
          marque_nom: 'BMW',
          modele_nom: 'Série 3',
          ville: 'Lyon',
          departement: '69',
          images: ['/images/bmw3-1.jpg'],
          est_bonne_affaire: true,
          pourcentage_economie: 8,
          date_publication: '2024-01-14',
          categorie: 'berline',
          puissance: 190,
          couleur: 'Blanc',
          description: 'BMW Série 3 très bien entretenue',
          vue_count: 856
        },
        {
          id: 3,
          titre: 'Renault Clio 2022',
          prix: 15400,
          prix_estime: 17500,
          kilometrage: 15000,
          annee: 2022,
          carburant: 'essence',
          boite_vitesse: 'manuelle',
          marque_nom: 'Renault',
          modele_nom: 'Clio',
          ville: 'Marseille',
          departement: '13',
          images: ['/images/clio-1.jpg'],
          est_bonne_affaire: true,
          pourcentage_economie: 12,
          date_publication: '2024-01-13',
          categorie: 'citadine',
          puissance: 90,
          couleur: 'Gris',
          description: 'Renault Clio récente',
          vue_count: 623
        }
      ]
      setAnnonces(mockData)
      setPagination(prev => ({ ...prev, total: mockData.length }))
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setPagination(prev => ({ ...prev, page: 1 }))
  }

  const resetFilters = () => {
    setFilters({
      marque: '',
      modele: '',
      prix_min: '',
      prix_max: '',
      km_max: '',
      annee_min: '',
      annee_max: '',
      carburant: '',
      boite_vitesse: '',
      categorie: '',
      departement: '',
      puissance_min: '',
      puissance_max: '',
      couleur: '',
      critair: '',
      garantie: false,
      controle_technique: false,
      premiere_main: false,
      non_fumeur: false
    })
    setSearchTerm('')
    setPagination(prev => ({ ...prev, page: 1 }))
  }

  const toggleFavorite = (annonceId) => {
    setFavorites(prev => 
      prev.includes(annonceId) 
        ? prev.filter(id => id !== annonceId)
        : [...prev, annonceId]
    )
  }

  const toggleSelection = (annonceId) => {
    setSelectedAnnonces(prev => 
      prev.includes(annonceId) 
        ? prev.filter(id => id !== annonceId)
        : [...prev, annonceId]
    )
  }

  const getActiveFiltersCount = () => {
    return Object.values(filters).filter(value => 
      value !== '' && value !== false && value !== null
    ).length
  }

  const filteredAnnonces = annonces.filter(annonce => {
    // Recherche textuelle
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase()
      if (!annonce.titre.toLowerCase().includes(searchLower) &&
          !annonce.marque_nom.toLowerCase().includes(searchLower) &&
          !annonce.modele_nom.toLowerCase().includes(searchLower) &&
          !annonce.description.toLowerCase().includes(searchLower)) {
        return false
      }
    }
    
    // Filtres standards
    if (filters.marque && !annonce.marque_nom.toLowerCase().includes(filters.marque.toLowerCase())) return false
    if (filters.modele && !annonce.modele_nom.toLowerCase().includes(filters.modele.toLowerCase())) return false
    if (filters.prix_min && annonce.prix < parseInt(filters.prix_min)) return false
    if (filters.prix_max && annonce.prix > parseInt(filters.prix_max)) return false
    if (filters.km_max && annonce.kilometrage > parseInt(filters.km_max)) return false
    if (filters.annee_min && annonce.annee < parseInt(filters.annee_min)) return false
    if (filters.annee_max && annonce.annee > parseInt(filters.annee_max)) return false
    if (filters.carburant && annonce.carburant !== filters.carburant) return false
    if (filters.boite_vitesse && annonce.boite_vitesse !== filters.boite_vitesse) return false
    if (filters.categorie && annonce.categorie !== filters.categorie) return false
    if (filters.departement && annonce.departement !== filters.departement) return false
    if (filters.puissance_min && annonce.puissance < parseInt(filters.puissance_min)) return false
    if (filters.puissance_max && annonce.puissance > parseInt(filters.puissance_max)) return false
    if (filters.couleur && !annonce.couleur.toLowerCase().includes(filters.couleur.toLowerCase())) return false
    
    return true
  }).sort((a, b) => {
    switch (sortBy) {
      case 'prix_asc':
        return a.prix - b.prix
      case 'prix_desc':
        return b.prix - a.prix
      case 'km_asc':
        return a.kilometrage - b.kilometrage
      case 'km_desc':
        return b.kilometrage - a.kilometrage
      case 'annee_desc':
        return b.annee - a.annee
      case 'economie':
        return b.pourcentage_economie - a.pourcentage_economie
      case 'popularite':
        return b.vue_count - a.vue_count
      default: // date_publication
        return new Date(b.date_publication) - new Date(a.date_publication)
    }
  })

  // Pagination
  const paginatedAnnonces = filteredAnnonces.slice(
    (pagination.page - 1) * pagination.limit,
    pagination.page * pagination.limit
  )

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Annonces automobiles</h1>
          <p className="text-primary-text-secondary">Découvrez notre sélection de véhicules d'occasion</p>
        </div>

        {/* Barre de recherche et filtres avancés */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
          {/* Barre de recherche principale */}
          <div className="flex flex-col lg:flex-row gap-4 mb-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary-text-secondary" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Rechercher une marque, un modèle, une description..."
                  className="w-full pl-10 pr-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                />
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                  getActiveFiltersCount() > 0
                    ? 'bg-accent text-white'
                    : 'bg-primary-elevated border border-primary-border/DEFAULT text-primary-text-primary hover:bg-primary-card'
                }`}
              >
                <Filter className="w-5 h-5" />
                <span>Filtres</span>
                {getActiveFiltersCount() > 0 && (
                  <span className="bg-accent-secondary text-white text-xs px-2 py-1 rounded-full">
                    {getActiveFiltersCount()}
                  </span>
                )}
                <ChevronDown className={`w-4 h-4 transform transition-transform ${showFilters ? 'rotate-180' : ''}`} />
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
            </div>
          </div>

          {/* Filtres avancés */}
          {showFilters && (
            <div className="space-y-6 pt-4 border-t border-primary-border/DEFAULT">
              {/* Filtres de base */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Marque</label>
                  <input
                    type="text"
                    value={filters.marque}
                    onChange={(e) => handleFilterChange('marque', e.target.value)}
                    placeholder="Ex: Peugeot"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Modèle</label>
                  <input
                    type="text"
                    value={filters.modele}
                    onChange={(e) => handleFilterChange('modele', e.target.value)}
                    placeholder="Ex: 208"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Catégorie</label>
                  <select
                    value={filters.categorie}
                    onChange={(e) => handleFilterChange('categorie', e.target.value)}
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
                  >
                    <option value="">Toutes</option>
                    <option value="citadine">Citadine</option>
                    <option value="compact">Compact</option>
                    <option value="berline">Berline</option>
                    <option value="suv">SUV</option>
                    <option value="monospace">Monospace</option>
                    <option value="utilitaire">Utilitaire</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Carburant</label>
                  <select
                    value={filters.carburant}
                    onChange={(e) => handleFilterChange('carburant', e.target.value)}
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
                  >
                    <option value="">Tous</option>
                    <option value="essence">Essence</option>
                    <option value="diesel">Diesel</option>
                    <option value="electrique">Électrique</option>
                    <option value="hybride">Hybride</option>
                  </select>
                </div>
              </div>

              {/* Prix et kilométrage */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Prix min</label>
                  <input
                    type="number"
                    value={filters.prix_min}
                    onChange={(e) => handleFilterChange('prix_min', e.target.value)}
                    placeholder="0€"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Prix max</label>
                  <input
                    type="number"
                    value={filters.prix_max}
                    onChange={(e) => handleFilterChange('prix_max', e.target.value)}
                    placeholder="50000€"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Kilométrage max</label>
                  <input
                    type="number"
                    value={filters.km_max}
                    onChange={(e) => handleFilterChange('km_max', e.target.value)}
                    placeholder="100000 km"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Département</label>
                  <input
                    type="text"
                    value={filters.departement}
                    onChange={(e) => handleFilterChange('departement', e.target.value)}
                    placeholder="75"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
              </div>

              {/* Filtres avancés */}
              <div>
                <button
                  onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                  className="flex items-center space-x-2 text-primary-text-secondary hover:text-primary-text-primary transition-colors duration-200 mb-4"
                >
                  <SlidersHorizontal className="w-4 h-4" />
                  <span>Filtres avancés</span>
                  <ChevronDown className={`w-4 h-4 transform transition-transform ${showAdvancedFilters ? 'rotate-180' : ''}`} />
                </button>
                
                {showAdvancedFilters && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-primary-text-secondary mb-2">Année min</label>
                      <input
                        type="number"
                        value={filters.annee_min}
                        onChange={(e) => handleFilterChange('annee_min', e.target.value)}
                        placeholder="2018"
                        className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-primary-text-secondary mb-2">Année max</label>
                      <input
                        type="number"
                        value={filters.annee_max}
                        onChange={(e) => handleFilterChange('annee_max', e.target.value)}
                        placeholder="2024"
                        className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-primary-text-secondary mb-2">Puissance min (ch)</label>
                      <input
                        type="number"
                        value={filters.puissance_min}
                        onChange={(e) => handleFilterChange('puissance_min', e.target.value)}
                        placeholder="90"
                        className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-primary-text-secondary mb-2">Couleur</label>
                      <input
                        type="text"
                        value={filters.couleur}
                        onChange={(e) => handleFilterChange('couleur', e.target.value)}
                        placeholder="Noir"
                        className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.garantie}
                      onChange={(e) => handleFilterChange('garantie', e.target.checked)}
                      className="w-4 h-4 text-accent bg-primary-elevated border-primary-border/DEFAULT rounded focus:ring-accent"
                    />
                    <span className="text-primary-text-primary">Garantie</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.premiere_main}
                      onChange={(e) => handleFilterChange('premiere_main', e.target.checked)}
                      className="w-4 h-4 text-accent bg-primary-elevated border-primary-border/DEFAULT rounded focus:ring-accent"
                    />
                    <span className="text-primary-text-primary">Première main</span>
                  </label>
                </div>
                <button
                  onClick={resetFilters}
                  className="flex items-center space-x-2 px-4 py-2 border border-primary-border/DEFAULT rounded-lg text-primary-text-secondary hover:bg-primary-elevated transition-colors duration-200"
                >
                  <X className="w-4 h-4" />
                  <span>Réinitialiser</span>
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Résultats et tri */}
        <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-4">
            <p className="text-primary-text-secondary">
              <span className="font-bold text-primary-text-primary">{filteredAnnonces.length}</span> annonce{filteredAnnonces.length > 1 ? 's' : ''} trouvée{filteredAnnonces.length > 1 ? 's' : ''}
            </p>
            {selectedAnnonces.length > 0 && (
              <span className="text-sm text-accent">
                {selectedAnnonces.length} sélectionnée{selectedAnnonces.length > 1 ? 's' : ''}
              </span>
            )}
          </div>
          
          <div className="flex items-center space-x-4">
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 bg-primary-card border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
            >
              <option value="date_publication">Plus récentes</option>
              <option value="prix_asc">Prix croissant</option>
              <option value="prix_desc">Prix décroissant</option>
              <option value="km_asc">Kilométrage croissant</option>
              <option value="km_desc">Kilométrage décroissant</option>
              <option value="annee_desc">Année décroissante</option>
              <option value="economie">Meilleures affaires</option>
              <option value="popularite">Plus populaires</option>
            </select>
            
            {selectedAnnonces.length > 1 && (
              <button className="px-4 py-2 bg-accent hover:bg-accent-secondary text-white rounded-lg font-medium transition-colors duration-200">
                Comparer ({selectedAnnonces.length})
              </button>
            )}
          </div>
        </div>

        {/* Grid des annonces */}
        {loading ? (
          <div className={`${viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'space-y-4'} gap-6`}>
            {[...Array(6)].map((_, index) => (
              <div key={index} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl overflow-hidden animate-pulse-slow">
                <div className="h-48 bg-primary-elevated"></div>
                <div className="p-4">
                  <div className="h-6 bg-primary-elevated rounded mb-2"></div>
                  <div className="h-4 bg-primary-elevated rounded mb-4"></div>
                  <div className="h-8 bg-primary-elevated rounded"></div>
                </div>
              </div>
            ))}
          </div>
        ) : paginatedAnnonces.length === 0 ? (
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-12 text-center">
            <Car className="w-16 h-16 text-primary-text-secondary mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-primary-text-primary mb-2">Aucune annonce trouvée</h3>
            <p className="text-primary-text-secondary mb-6">
              {searchTerm || getActiveFiltersCount() > 0 
                ? 'Essayez de modifier vos critères de recherche'
                : 'Aucune annonce disponible pour le moment'
              }
            </p>
            {(searchTerm || getActiveFiltersCount() > 0) && (
              <button
                onClick={resetFilters}
                className="bg-accent hover:bg-accent-secondary text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
              >
                Réinitialiser les filtres
              </button>
            )}
          </div>
        ) : (
          <>
            <div className={`${viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'space-y-4'} gap-6`}>
              {paginatedAnnonces.map((annonce) => (
                <div key={annonce.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl overflow-hidden hover:shadow-card-hover transition-all duration-300 group">
                  {/* Header carte */}
                  <div className="relative">
                    {/* Badge bonne affaire */}
                    {annonce.est_bonne_affaire && (
                      <div className="absolute top-2 left-2 bg-success text-white text-xs font-bold px-2 py-1 rounded-full z-10">
                        Bonne affaire
                      </div>
                    )}
                    
                    {/* Checkbox sélection */}
                    <div className="absolute top-2 right-2 z-10">
                      <button
                        onClick={() => toggleSelection(annonce.id)}
                        className={`p-2 rounded-lg border transition-all duration-200 ${
                          selectedAnnonces.includes(annonce.id)
                            ? 'bg-accent border-accent text-white'
                            : 'bg-white/90 border-primary-border/DEFAULT text-primary-text-secondary hover:bg-white'
                        }`}
                      >
                        {selectedAnnonces.includes(annonce.id) && <Check className="w-4 h-4" />}
                      </button>
                    </div>
                    
                    {/* Image */}
                    <div className="relative h-48 bg-primary-elevated">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-6xl text-primary-text-secondary">🚗</div>
                      </div>
                      
                      {/* Overlay avec actions */}
                      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center space-x-2">
                        <button className="p-2 bg-white rounded-lg text-primary-text-primary hover:bg-accent hover:text-white transition-colors duration-200">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button 
                          onClick={() => toggleFavorite(annonce.id)}
                          className={`p-2 rounded-lg transition-colors duration-200 ${
                            favorites.includes(annonce.id)
                              ? 'bg-accent text-white'
                              : 'bg-white text-primary-text-primary hover:bg-accent hover:text-white'
                          }`}
                        >
                          <Heart className={`w-4 h-4 ${favorites.includes(annonce.id) ? 'fill-current' : ''}`} />
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  {/* Contenu */}
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-primary-text-primary line-clamp-2">{annonce.titre}</h3>
                      <button 
                        onClick={() => toggleFavorite(annonce.id)}
                        className={`ml-2 p-1 rounded transition-colors duration-200 ${
                          favorites.includes(annonce.id)
                            ? 'text-accent'
                            : 'text-primary-text-secondary hover:text-accent'
                        }`}
                      >
                        <Heart className={`w-4 h-4 ${favorites.includes(annonce.id) ? 'fill-current' : ''}`} />
                      </button>
                    </div>
                    
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-2xl font-bold text-primary-text-primary">{annonce.prix.toLocaleString()}€</span>
                      {annonce.est_bonne_affaire && (
                        <span className="text-sm text-success font-medium">-{annonce.pourcentage_economie}%</span>
                      )}
                    </div>
                    
                    {/* Caractéristiques */}
                    <div className="grid grid-cols-2 gap-2 text-sm text-primary-text-secondary mb-3">
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{annonce.annee}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Settings className="w-4 h-4" />
                        <span>{(annonce.kilometrage / 1000).toFixed(0)}k km</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Fuel className="w-4 h-4" />
                        <span className="capitalize">{annonce.carburant}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4" />
                        <span>{annonce.ville}</span>
                      </div>
                    </div>
                    
                    {/* Stats additionnelles */}
                    <div className="flex items-center justify-between text-xs text-primary-text-secondary mb-3">
                      <div className="flex items-center space-x-1">
                        <Eye className="w-3 h-3" />
                        <span>{annonce.vue_count}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="w-3 h-3" />
                        <span>{new Date(annonce.date_publication).toLocaleDateString('fr-FR')}</span>
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex space-x-2">
                      <button className="flex-1 bg-accent hover:bg-accent-secondary text-white py-2 rounded-lg font-medium transition-colors duration-200">
                        Voir détails
                      </button>
                      <button className="p-2 border border-accent text-accent hover:bg-accent hover:text-white rounded-lg transition-all duration-200">
                        <Heart className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Pagination */}
            {pagination.total > pagination.limit && (
              <div className="flex justify-center items-center space-x-2 mt-8">
                <button
                  onClick={() => setPagination(prev => ({ ...prev, page: Math.max(1, prev.page - 1) }))}
                  disabled={pagination.page === 1}
                  className="p-2 border border-primary-border/DEFAULT rounded-lg text-primary-text-secondary hover:bg-primary-elevated disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                
                {Array.from({ length: Math.min(5, Math.ceil(pagination.total / pagination.limit)) }, (_, index) => {
                  const pageNumber = index + 1
                  const totalPages = Math.ceil(pagination.total / pagination.limit)
                  const currentPage = pagination.page
                  
                  // Afficher les pages autour de la page actuelle
                  let showPage = false
                  if (totalPages <= 5) {
                    showPage = true
                  } else if (pageNumber === 1 || pageNumber === totalPages) {
                    showPage = true
                  } else if (Math.abs(pageNumber - currentPage) <= 1) {
                    showPage = true
                  }
                  
                  if (showPage) {
                    return (
                      <button
                        key={pageNumber}
                        onClick={() => setPagination(prev => ({ ...prev, page: pageNumber }))}
                        className={`px-3 py-1 rounded-lg font-medium transition-colors duration-200 ${
                          pagination.page === pageNumber
                            ? 'bg-accent text-white'
                            : 'border border-primary-border/DEFAULT text-primary-text-secondary hover:bg-primary-elevated'
                        }`}
                      >
                        {pageNumber}
                      </button>
                    )
                  }
                  return null
                })}
                
                <button
                  onClick={() => setPagination(prev => ({ ...prev, page: Math.min(Math.ceil(prev.total / prev.limit), prev.page + 1) }))}
                  disabled={pagination.page === Math.ceil(pagination.total / pagination.limit)}
                  className="p-2 border border-primary-border/DEFAULT rounded-lg text-primary-text-secondary hover:bg-primary-elevated disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
