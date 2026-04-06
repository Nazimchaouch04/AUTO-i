import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Heart, Share2, Phone, Mail, MapPin, Calendar, Fuel, Settings, Shield, Star, ChevronLeft, ChevronRight, Maximize2, Download, Camera, Video, FileText, AlertCircle, Check, X, Send, MessageSquare, ExternalLink, TrendingUp, Award, Clock, Users, Zap, Swords } from 'lucide-react'

export default function AnnonceDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [annonce, setAnnonce] = useState(null)
  const [loading, setLoading] = useState(true)
  const [currentImage, setCurrentImage] = useState(0)
  const [showContact, setShowContact] = useState(false)
  const [isFavorite, setIsFavorite] = useState(false)
  const [showShareModal, setShowShareModal] = useState(false)
  const [showImageModal, setShowImageModal] = useState(false)
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)
  const [activeTab, setActiveTab] = useState('description')
  const [message, setMessage] = useState('')
  const [showMessageForm, setShowMessageForm] = useState(false)
  const [similarAnnonces, setSimilarAnnonces] = useState([])
  const [viewHistory, setViewHistory] = useState([])
  const [showCompareModal, setShowCompareModal] = useState(false)
  const [recentVehicles, setRecentVehicles] = useState([])

  useEffect(() => {
    fetchAnnonceDetail()
  }, [id])

  const fetchAnnonceDetail = async () => {
    setLoading(true)
    try {
      // Connexion à l'API Django
      const response = await fetch(`http://127.0.0.1:8000/api/annonces/${id}/`)
      if (!response.ok) throw new Error('Failed to fetch annonce detail')
      
      const data = await response.json()
      
      // Transformer les données pour correspondre au format attendu
      const transformedAnnonce = {
        id: data.id,
        titre: data.titre,
        description: data.description || 'Magnifique véhicule en excellent état.',
        prix: data.prix,
        prix_estime: data.prix_estime || Math.round(data.prix * 1.15),
        kilometrage: data.kilometrage,
        annee: data.annee,
        carburant: data.carburant,
        boite_vitesse: data.boite_vitesse,
        puissance: data.puissance || 130,
        couleur: data.couleur || 'Noir',
        marque_nom: data.marque_nom || 'Peugeot',
        modele_nom: data.modele_nom || '208',
        ville: data.ville || 'Paris',
        departement: data.departement || '75',
        images: data.images || [
          '/images/peugeot208-1.jpg',
          '/images/peugeot208-2.jpg',
          '/images/peugeot208-3.jpg',
          '/images/peugeot208-4.jpg'
        ],
        est_bonne_affaire: data.est_bonne_affaire || false,
        pourcentage_economie: data.pourcentage_economie || 0,
        economie_potentielle: data.economie_potentielle || Math.round(data.prix * 0.15),
        fiabilite_score: data.fiabilite_score || 85,
        date_publication: data.date_publication || '2024-01-15',
        vue_count: data.vue_count || 1234,
        nom_vendeur: data.nom_vendeur || 'Jean Dupont',
        telephone: data.telephone || '06 12 34 56 78',
        email: data.email || 'jean.dupont@email.com',
        professionnel: data.professionnel || false,
        caracteristiques: {
          'marque': data.marque_nom || 'Peugeot',
          'modele': data.modele_nom || '208',
          'version': 'GT Line',
          'energie': data.carburant || 'Essence',
          'boite_vitesse': data.boite_vitesse || 'Manuelle',
          'puissance': `${data.puissance || 130} ch`,
          'couleur': data.couleur || 'Noir',
          'portes': 5,
          'places': 5,
          'critair': 2,
          'km': data.kilometrage || 25000,
          'annee': data.annee || 2021,
          'mise_en_circulation': '15/03/2021',
          'garantie': 'Oui (jusqu\'au 15/03/2024)',
          'controle_technique': 'OK (15/01/2024)'
        },
        options: data.options || [
          'GPS intégré',
          'Climatisation automatique',
          'Radars de recul',
          'Caméra de recul',
          'Bluetooth',
          'USB',
          'Régulateur de vitesse',
          'Allumage automatique des feux',
          'Détecteur de fatigue',
          'Aide au stationnement'
        ],
        videos: data.videos || [],
        documents: data.documents || [
          { nom: 'Contrôle technique', url: '/docs/ct.pdf', type: 'pdf' },
          { nom: 'Carte grise', url: '/docs/carte-grise.pdf', type: 'pdf' },
          { nom: 'Facture d\'entretien', url: '/docs/facture.pdf', type: 'pdf' }
        ]
      }
      
      setAnnonce(transformedAnnonce)
      setIsFavorite(data.is_favorite)
      
      // Charger les annonces similaires
      fetchSimilarAnnonces()
      
      // Enregistrer la vue
      recordView(transformedAnnonce.id)
      
    } catch (error) {
      console.error('Error fetching annonce detail:', error)
      // Fallback vers données simulées
      const mockData = {
        id: parseInt(id),
        titre: 'Peugeot 208 GT Line 2021',
        description: 'Magnifique Peugeot 208 GT Line de 2021, très bien entretenue, première main. Équipements : GPS, climatisation automatique, radars de recul, caméra de recul, Bluetooth, USB. Contrôle technique OK. Garantie constructeur restante. Non-fumeur.',
        prix: 18500,
        prix_estime: 22000,
        kilometrage: 25000,
        annee: 2021,
        carburant: 'essence',
        boite_vitesse: 'manuelle',
        puissance: 130,
        couleur: 'Noir',
        marque_nom: 'Peugeot',
        modele_nom: '208',
        ville: 'Paris',
        departement: '75',
        images: [
          '/images/peugeot208-1.jpg',
          '/images/peugeot208-2.jpg',
          '/images/peugeot208-3.jpg',
          '/images/peugeot208-4.jpg'
        ],
        est_bonne_affaire: true,
        pourcentage_economie: 19,
        economie_potentielle: 3500,
        fiabilite_score: 85,
        date_publication: '2024-01-15',
        vue_count: 1234,
        nom_vendeur: 'Jean Dupont',
        telephone: '06 12 34 56 78',
        email: 'jean.dupont@email.com',
        professionnel: false,
        caracteristiques: {
          'marque': 'Peugeot',
          'modele': '208',
          'version': 'GT Line',
          'energie': 'Essence',
          'boite_vitesse': 'Manuelle',
          'puissance': '130 ch',
          'couleur': 'Noir',
          'portes': 5,
          'places': 5,
          'critair': 2,
          'km': 25000,
          'annee': 2021,
          'mise_en_circulation': '15/03/2021',
          'garantie': 'Oui (jusqu\'au 15/03/2024)',
          'controle_technique': 'OK (15/01/2024)'
        },
        options: [
          'GPS intégré',
          'Climatisation automatique',
          'Radars de recul',
          'Caméra de recul',
          'Bluetooth',
          'USB',
          'Régulateur de vitesse',
          'Allumage automatique des feux',
          'Détecteur de fatigue',
          'Aide au stationnement'
        ],
        videos: [],
        documents: [
          { nom: 'Contrôle technique', url: '/docs/ct.pdf', type: 'pdf' },
          { nom: 'Carte grise', url: '/docs/carte-grise.pdf', type: 'pdf' },
          { nom: 'Facture d\'entretien', url: '/docs/facture.pdf', type: 'pdf' }
        ]
      }
      setAnnonce(mockData)
      fetchSimilarAnnonces(mockData)
    } finally {
      setLoading(false)
    }
  }

  const fetchSimilarAnnonces = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/annonces/${id}/similaires/`)
      if (response.ok) {
        const data = await response.json()
        setSimilarAnnonces(data)
      }
    } catch (error) {
      console.error('Error fetching similar annonces:', error)
    }
  }

  const recordView = async (annonceId) => {
    try {
      // Enregistrer la vue dans l'historique local
      const history = JSON.parse(localStorage.getItem('viewHistory') || '[]')
      const newHistory = [annonceId, ...history.filter(id => id !== annonceId)].slice(0, 20)
      localStorage.setItem('viewHistory', JSON.stringify(newHistory))
      setViewHistory(newHistory)
    } catch (error) {
      console.error('Error recording view:', error)
    }
  }

  const nextImage = () => {
    setCurrentImage((prev) => (prev + 1) % annonce.images.length)
  }

  const prevImage = () => {
    setCurrentImage((prev) => (prev - 1 + annonce.images.length) % annonce.images.length)
  }

  const openImageModal = (index) => {
    setSelectedImageIndex(index)
    setShowImageModal(true)
  }

  const toggleFavorite = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/annonces/${id}/toggle_favori/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setIsFavorite(data.status === 'added')
      }
    } catch (error) {
      console.error('Error toggling favorite:', error)
    }
  }

  const shareAnnonce = (platform) => {
    const url = window.location.href
    const text = `Découvrez cette annonce: ${annonce.titre} - ${annonce.prix.toLocaleString()}€`
    
    switch (platform) {
      case 'facebook':
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank')
        break
      case 'twitter':
        window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank')
        break
      case 'whatsapp':
        window.open(`https://wa.me/?text=${text} ${url}`, '_blank')
        break
      case 'copy':
        navigator.clipboard.writeText(`${text} ${url}`)
        alert('Lien copié dans le presse-papiers!')
        break
    }
    setShowShareModal(false)
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!message.trim()) return
    
    try {
      // Envoyer le message via l'API
      const response = await fetch(`http://127.0.0.1:8000/api/annonces/${annonce.id}/contact/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message })
      })
      
      if (response.ok) {
        alert('Message envoyé avec succès!')
        setMessage('')
        setShowMessageForm(false)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      alert('Erreur lors de l\'envoi du message')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse-slow">
            <div className="h-64 bg-primary-card rounded-xl mb-8"></div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <div className="h-8 bg-primary-card rounded mb-4"></div>
                <div className="h-4 bg-primary-card rounded mb-2"></div>
                <div className="h-4 bg-primary-card rounded mb-4"></div>
                <div className="h-64 bg-primary-card rounded"></div>
              </div>
              <div className="h-96 bg-primary-card rounded"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!annonce) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-primary-text-primary mb-4">Annonce non trouvée</h1>
            <button
              onClick={() => navigate('/annonces')}
              className="bg-accent hover:bg-accent-secondary text-white px-6 py-2 rounded-lg transition-colors duration-200"
            >
              Retour aux annonces
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => navigate('/annonces')}
            className="flex items-center space-x-2 text-primary-text-secondary hover:text-primary-text-primary transition-colors duration-200"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Retour aux annonces</span>
          </button>
          <div className="flex items-center space-x-2">
            <button 
              onClick={toggleFavorite}
              className={`p-2 border rounded-lg transition-colors duration-200 ${
                isFavorite 
                  ? 'bg-accent border-accent text-white' 
                  : 'border-primary-border/DEFAULT text-primary-text-secondary hover:bg-primary-elevated'
              }`}
            >
              <Heart className={`w-5 h-5 ${isFavorite ? 'fill-current' : ''}`} />
            </button>
            <button 
              onClick={() => setShowShareModal(true)}
              className="p-2 border border-primary-border/DEFAULT rounded-lg hover:bg-primary-elevated transition-colors duration-200"
            >
              <Share2 className="w-5 h-5 text-primary-text-secondary" />
            </button>
            <button 
              onClick={() => setShowCompareModal(true)}
              className="p-2 border border-primary-border/DEFAULT rounded-lg hover:bg-accent hover:border-accent hover:text-white transition-all duration-200 group relative"
              title="Comparer avec un autre véhicule"
            >
              <Swords className="w-5 h-5" />
              <span className="absolute -top-10 left-1/2 -translate-x-1/2 bg-accent text-white text-[10px] font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                Comparer (+10 AC)
              </span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Colonne principale */}
          <div className="lg:col-span-2 space-y-8">
            {/* Galerie d'images améliorée */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl overflow-hidden">
              <div className="relative h-96 bg-primary-elevated group">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-8xl text-primary-text-secondary">🚗</div>
                </div>
                
                {/* Bouton plein écran */}
                <button
                  onClick={() => openImageModal(currentImage)}
                  className="absolute top-4 right-4 p-2 bg-black/50 text-white rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-black/70"
                >
                  <Maximize2 className="w-4 h-4" />
                </button>
                
                {/* Badge bonne affaire */}
                {annonce.est_bonne_affaire && (
                  <div className="absolute top-4 left-4 bg-success text-white px-3 py-1 rounded-full text-sm font-bold">
                    Bonne affaire
                  </div>
                )}
                
                {/* Counter images */}
                {annonce.images.length > 1 && (
                  <div className="absolute bottom-4 left-4 bg-black/50 text-white px-2 py-1 rounded text-sm">
                    {currentImage + 1} / {annonce.images.length}
                  </div>
                )}
                
                {/* Boutons navigation */}
                {annonce.images.length > 1 && (
                  <>
                    <button
                      onClick={prevImage}
                      className="absolute left-4 top-1/2 transform -translate-y-1/2 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors duration-200"
                    >
                      <ChevronLeft className="w-6 h-6" />
                    </button>
                    <button
                      onClick={nextImage}
                      className="absolute right-4 top-1/2 transform -translate-y-1/2 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors duration-200"
                    >
                      <ChevronRight className="w-6 h-6" />
                    </button>
                  </>
                )}
              </div>
              
              {/* Thumbnails */}
              {annonce.images.length > 1 && (
                <div className="flex space-x-2 p-4 overflow-x-auto">
                  {annonce.images.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentImage(index)}
                      className={`flex-shrink-0 w-20 h-20 bg-primary-elevated rounded-lg border-2 transition-all duration-200 ${
                        currentImage === index ? 'border-accent' : 'border-primary-border/DEFAULT'
                      }`}
                    >
                      <div className="w-full h-full flex items-center justify-center text-2xl text-primary-text-secondary">
                        🚗
                      </div>
                    </button>
                  ))}
                </div>
              )}
              
              {/* Barre d'outils */}
              <div className="flex items-center justify-between p-4 border-t border-primary-border/DEFAULT">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                    <Camera className="w-4 h-4" />
                    <span>{annonce.images.length} photo{annonce.images.length > 1 ? 's' : ''}</span>
                  </div>
                  {annonce.videos && annonce.videos.length > 0 && (
                    <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                      <Video className="w-4 h-4" />
                      <span>{annonce.videos.length} vidéo{annonce.videos.length > 1 ? 's' : ''}</span>
                    </div>
                  )}
                </div>
                <button className="flex items-center space-x-2 text-sm text-accent hover:text-accent-secondary transition-colors duration-200">
                  <Download className="w-4 h-4" />
                  <span>Télécharger</span>
                </button>
              </div>
            </div>

            {/* Informations principales avec tabs */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl overflow-hidden">
              {/* Tabs */}
              <div className="flex border-b border-primary-border/DEFAULT">
                {['description', 'caracteristiques', 'options', 'documents'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`flex-1 px-4 py-3 text-sm font-medium transition-colors duration-200 ${
                      activeTab === tab
                        ? 'bg-accent text-white'
                        : 'text-primary-text-secondary hover:bg-primary-elevated'
                    }`}
                  >
                    {tab === 'description' && 'Description'}
                    {tab === 'caracteristiques' && 'Caractéristiques'}
                    {tab === 'options' && 'Options'}
                    {tab === 'documents' && 'Documents'}
                  </button>
                ))}
              </div>
              
              <div className="p-6">
                {/* Tab Description */}
                {activeTab === 'description' && (
                  <div>
                    <h2 className="text-xl font-semibold text-primary-text-primary mb-4">{annonce.titre}</h2>
                    
                    {/* Prix et économie */}
                    <div className="flex items-center justify-between mb-6">
                      <div>
                        <div className="text-3xl font-bold text-primary-text-primary">{annonce.prix.toLocaleString()}€</div>
                        {annonce.est_bonne_affaire && (
                          <div className="mt-2 flex items-center space-x-2">
                            <span className="text-sm text-primary-text-secondary">Estimation: </span>
                            <span className="text-lg font-bold text-accent">{annonce.prix_estime.toLocaleString()}€</span>
                            <span className="bg-success text-white px-2 py-1 rounded text-sm font-bold">
                              -{annonce.pourcentage_economie}%
                            </span>
                          </div>
                        )}
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-primary-text-secondary">Économie potentielle</div>
                        <div className="text-xl font-bold text-success">{annonce.economie_potentielle.toLocaleString()}€</div>
                      </div>
                    </div>
                    
                    {/* Caractéristiques principales */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                      <div className="flex items-center space-x-2">
                        <Calendar className="w-5 h-5 text-primary-text-secondary" />
                        <div>
                          <div className="text-sm text-primary-text-secondary">Année</div>
                          <div className="font-medium text-primary-text-primary">{annonce.annee}</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Settings className="w-5 h-5 text-primary-text-secondary" />
                        <div>
                          <div className="text-sm text-primary-text-secondary">Kilométrage</div>
                          <div className="font-medium text-primary-text-primary">{annonce.kilometrage.toLocaleString()} km</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Fuel className="w-5 h-5 text-primary-text-secondary" />
                        <div>
                          <div className="text-sm text-primary-text-secondary">Carburant</div>
                          <div className="font-medium text-primary-text-primary capitalize">{annonce.carburant}</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Shield className="w-5 h-5 text-primary-text-secondary" />
                        <div>
                          <div className="text-sm text-primary-text-secondary">Fiabilité</div>
                          <div className="font-medium text-primary-text-primary">{annonce.fiabilite_score}/100</div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Description */}
                    <div>
                      <h3 className="text-lg font-semibold text-primary-text-primary mb-3">Description</h3>
                      <p className="text-primary-text-secondary leading-relaxed">{annonce.description}</p>
                    </div>
                  </div>
                )}
                
                {/* Tab Caractéristiques */}
                {activeTab === 'caracteristiques' && (
                  <div>
                    <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Caractéristiques techniques</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(annonce.caracteristiques).map(([key, value]) => (
                        <div key={key} className="flex justify-between py-2 border-b border-primary-border/DEFAULT">
                          <span className="text-primary-text-secondary capitalize">
                            {key.replace('_', ' ')}
                          </span>
                          <span className="font-medium text-primary-text-primary">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Tab Options */}
                {activeTab === 'options' && (
                  <div>
                    <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Options et équipements</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {annonce.options.map((option, index) => (
                        <div key={index} className="flex items-center space-x-3 p-3 bg-primary-elevated rounded-lg">
                          <div className="w-2 h-2 bg-accent rounded-full"></div>
                          <span className="text-primary-text-primary">{option}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Tab Documents */}
                {activeTab === 'documents' && (
                  <div>
                    <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Documents disponibles</h3>
                    <div className="space-y-3">
                      {annonce.documents.map((doc, index) => (
                        <div key={index} className="flex items-center justify-between p-4 bg-primary-elevated rounded-lg">
                          <div className="flex items-center space-x-3">
                            <FileText className="w-5 h-5 text-primary-text-secondary" />
                            <div>
                              <p className="font-medium text-primary-text-primary">{doc.nom}</p>
                              <p className="text-sm text-primary-text-secondary">{doc.type.toUpperCase()}</p>
                            </div>
                          </div>
                          <button className="flex items-center space-x-2 px-4 py-2 bg-accent hover:bg-accent-secondary text-white rounded-lg transition-colors duration-200">
                            <ExternalLink className="w-4 h-4" />
                            <span>Voir</span>
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Colonne latérale */}
          <div className="space-y-6">
            {/* Carte vendeur */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
              <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Vendeur</h3>
              
              <div className="mb-4">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center text-white font-bold">
                    {annonce.nom_vendeur.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <div className="font-medium text-primary-text-primary">{annonce.nom_vendeur}</div>
                    <div className="text-sm text-primary-text-secondary">
                      {annonce.professionnel ? 'Professionnel' : 'Particulier'}
                    </div>
                  </div>
                </div>
                
                <div className="space-y-2 text-sm text-primary-text-secondary">
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-4 h-4" />
                    <span>{annonce.ville} ({annonce.departement})</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4" />
                    <span>Membre depuis Janvier 2024</span>
                  </div>
                </div>
              </div>
              
              {!showContact ? (
                <button
                  onClick={() => setShowContact(true)}
                  className="w-full bg-accent hover:bg-accent-secondary text-white py-3 rounded-lg font-medium transition-colors duration-200"
                >
                  Afficher le contact
                </button>
              ) : (
                <div className="space-y-3">
                  <button className="w-full bg-success hover:bg-success/90 text-white py-3 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2">
                    <Phone className="w-5 h-5" />
                    <span>{annonce.telephone}</span>
                  </button>
                  <button 
                    onClick={() => setShowMessageForm(true)}
                    className="w-full bg-primary-elevated hover:bg-primary-elevated/90 text-primary-text-primary py-3 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
                  >
                    <MessageSquare className="w-5 h-5" />
                    <span>Envoyer un message</span>
                  </button>
                </div>
              )}
            </div>

            {/* Carte estimation */}
            {annonce.est_bonne_affaire && (
              <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
                <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Estimation AutoIntel</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-primary-text-secondary">Prix demandé</span>
                    <span className="font-medium text-primary-text-primary">{annonce.prix.toLocaleString()}€</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-primary-text-secondary">Prix estimé</span>
                    <span className="font-medium text-accent">{annonce.prix_estime.toLocaleString()}€</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-primary-text-secondary">Économie</span>
                    <span className="font-medium text-success">{annonce.economie_potentielle.toLocaleString()}€</span>
                  </div>
                </div>
                
                <div className="mt-4 p-3 bg-success/10 rounded-lg">
                  <div className="flex items-center space-x-2 text-success">
                    <Star className="w-5 h-5" />
                    <span className="font-medium">Excellente affaire</span>
                  </div>
                  <p className="text-sm text-primary-text-secondary mt-1">
                    Ce véhicule est proposé {annonce.pourcentage_economie}% sous sa valeur estimée
                  </p>
                </div>
              </div>
            )}

            {/* Statistiques améliorées */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
              <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Statistiques</h3>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-2">
                    <Eye className="w-4 h-4 text-primary-text-secondary" />
                    <span className="text-primary-text-secondary">Vues</span>
                  </div>
                  <span className="font-medium text-primary-text-primary">{annonce.vue_count}</span>
                </div>
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4 text-primary-text-secondary" />
                    <span className="text-primary-text-secondary">Publié le</span>
                  </div>
                  <span className="font-medium text-primary-text-primary">{new Date(annonce.date_publication).toLocaleDateString('fr-FR')}</span>
                </div>
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="w-4 h-4 text-primary-text-secondary" />
                    <span className="text-primary-text-secondary">Popularité</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className={`w-3 h-3 ${i < Math.floor(annonce.vue_count / 200) ? 'text-warning fill-current' : 'text-primary-border/DEFAULT'}`} />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Annonces similaires */}
            {similarAnnonces.length > 0 && (
              <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
                <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Annonces similaires</h3>
                <div className="space-y-3">
                  {similarAnnonces.map((similar) => (
                    <div key={similar.id} className="flex items-center space-x-3 p-3 bg-primary-elevated rounded-lg hover:bg-primary-card transition-colors duration-200 cursor-pointer">
                      <div className="w-16 h-16 bg-primary-border/DEFAULT rounded-lg flex items-center justify-center text-2xl">
                        🚗
                      </div>
                      <div className="flex-1">
                        <h4 className="font-medium text-primary-text-primary text-sm">{similar.titre}</h4>
                        <div className="flex items-center space-x-2 text-xs text-primary-text-secondary">
                          <span>{similar.annee}</span>
                          <span>•</span>
                          <span>{(similar.kilometrage / 1000).toFixed(0)}k km</span>
                          <span>•</span>
                          <span>{similar.ville}</span>
                        </div>
                        <p className="font-bold text-accent text-sm">{similar.prix.toLocaleString()}€</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Modal de partage */}
        {showShareModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-[2rem] p-8 max-w-md w-full shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-white tracking-tight">Partager cette annonce</h3>
                <button
                  onClick={() => setShowShareModal(false)}
                  className="p-2 hover:bg-primary-elevated rounded-xl transition-colors"
                >
                  <X className="w-5 h-5 text-primary-text-secondary" />
                </button>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => shareAnnonce('facebook')}
                  className="flex flex-col items-center gap-2 p-4 bg-blue-600/10 hover:bg-blue-600/20 border border-blue-600/20 rounded-2xl text-blue-500 transition-all font-bold"
                >
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white"><Users size={20} /></div>
                  Facebook
                </button>
                <button
                  onClick={() => shareAnnonce('twitter')}
                  className="flex flex-col items-center gap-2 p-4 bg-sky-500/10 hover:bg-sky-500/20 border border-sky-500/20 rounded-2xl text-sky-500 transition-all font-bold"
                >
                  <div className="w-10 h-10 bg-sky-500 rounded-full flex items-center justify-center text-white"><Share2 size={20} /></div>
                  Twitter
                </button>
                <button
                  onClick={() => shareAnnonce('whatsapp')}
                  className="flex flex-col items-center gap-2 p-4 bg-green-600/10 hover:bg-green-600/20 border border-green-600/20 rounded-2xl text-green-500 transition-all font-bold"
                >
                  <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center text-white"><MessageSquare size={20} /></div>
                  WhatsApp
                </button>
                <button
                  onClick={() => shareAnnonce('copy')}
                  className="flex flex-col items-center gap-2 p-4 bg-primary-elevated hover:bg-primary-card border border-primary-border/DEFAULT rounded-2xl text-primary-text-primary transition-all font-bold"
                >
                  <div className="w-10 h-10 bg-primary-border/50 rounded-full flex items-center justify-center text-white"><FileText size={20} /></div>
                  Copier
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Modal d'image plein écran */}
        {showImageModal && (
          <div className="fixed inset-0 bg-black/95 flex items-center justify-center z-[100] p-4">
            <button
              onClick={() => setShowImageModal(false)}
              className="absolute top-8 right-8 p-3 bg-white/10 hover:bg-white/20 text-white rounded-full transition-all"
            >
              <X size={24} />
            </button>

            <div className="relative max-w-5xl w-full h-full flex flex-col items-center justify-center">
              <div className="relative group w-full flex items-center justify-center">
                 <img 
                  src={annonce.images[selectedImageIndex]} 
                  alt={annonce.titre}
                  className="max-w-full max-h-[80vh] rounded-3xl shadow-2xl object-contain"
                />
                
                {annonce.images.length > 1 && (
                  <>
                    <button
                      onClick={() => setSelectedImageIndex((prev) => (prev - 1 + annonce.images.length) % annonce.images.length)}
                      className="absolute left-4 p-4 bg-black/50 text-white rounded-full hover:bg-accent transition-all"
                    >
                      <ChevronLeft size={32} />
                    </button>
                    <button
                      onClick={() => setSelectedImageIndex((prev) => (prev + 1) % annonce.images.length)}
                      className="absolute right-4 p-4 bg-black/50 text-white rounded-full hover:bg-accent transition-all"
                    >
                      <ChevronRight size={32} />
                    </button>
                  </>
                )}
              </div>
              
              <div className="mt-8 flex gap-2 overflow-x-auto pb-4 max-w-4xl px-4">
                {annonce.images.map((img, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImageIndex(index)}
                    className={`flex-shrink-0 w-20 h-20 bg-primary-card rounded-xl border-2 overflow-hidden transition-all ${
                      selectedImageIndex === index ? 'border-accent scale-110' : 'border-transparent opacity-50 hover:opacity-100'
                    }`}
                  >
                    <img src={img} className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {/* Modal de messagerie */}
        {showMessageForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-[2.5rem] p-8 max-w-md w-full shadow-2xl">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-2xl font-black text-white tracking-tight">Contacter l'annonceur</h3>
                <button
                  onClick={() => setShowMessageForm(false)}
                  className="p-2 hover:bg-primary-elevated rounded-xl transition-colors"
                >
                  <X className="w-6 h-6 text-primary-text-secondary" />
                </button>
              </div>
              
              <form onSubmit={sendMessage} className="space-y-6">
                <div>
                  <label className="block text-xs font-bold text-primary-text-secondary uppercase tracking-[0.2em] mb-3">Votre message</label>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Bonjour, je suis intéressé par votre annonce. Le prix est-il négociable ?"
                    rows={5}
                    className="w-full px-6 py-4 bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl text-white placeholder-primary-text-secondary focus:outline-none focus:border-accent resize-none transition-all"
                    required
                  />
                </div>
                
                <button
                  type="submit"
                  className="w-full py-5 bg-accent hover:bg-accent-secondary text-white rounded-2xl font-black text-sm uppercase tracking-widest transition-all shadow-xl shadow-accent/20 flex items-center justify-center gap-3"
                >
                  <Send className="w-5 h-5" />
                  Envoyer le message
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Modal de Comparaison */}
        {showCompareModal && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-[100] p-4 animate-fade-in">
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-[3rem] p-10 max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-[0_0_100px_rgba(0,180,216,0.15)] relative">
              <div className="absolute top-0 right-0 p-10 opacity-5">
                 <Swords size={200} />
              </div>
              
              <div className="flex items-center justify-between mb-10 relative z-10">
                <div>
                   <h3 className="text-3xl font-black text-white tracking-tight uppercase">Arena Duel</h3>
                   <p className="text-sm text-primary-text-secondary mt-1">Choisissez un adversaire pour une analyse IA.</p>
                </div>
                <button
                  onClick={() => setShowCompareModal(false)}
                  className="p-3 bg-primary-elevated hover:bg-primary-card rounded-2xl transition-all border border-primary-border/DEFAULT"
                >
                  <X className="w-6 h-6 text-white" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto pr-4 space-y-6 relative z-10 custom-scrollbar">
                <div className="p-6 bg-accent/10 border border-accent/20 rounded-[2rem] flex items-center gap-4">
                   <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center text-white"><Zap size={24} /></div>
                   <div>
                      <p className="text-[10px] font-black text-accent uppercase tracking-widest">Véhicule Actuel</p>
                      <p className="text-xl font-bold text-white">{annonce.titre}</p>
                   </div>
                </div>

                <div className="flex items-center gap-4 mb-4">
                   <div className="h-[1px] flex-1 bg-white/10" />
                   <span className="text-[10px] font-black text-primary-text-secondary uppercase tracking-[0.3em]">Candidats suggérés</span>
                   <div className="h-[1px] flex-1 bg-white/10" />
                </div>

                {similarAnnonces.length > 0 ? (
                  similarAnnonces.map((similar) => (
                    <button
                      key={similar.id}
                      onClick={async () => {
                        try {
                           fetch('http://127.0.0.1:8000/api/gamification/profil/add-coins/', {
                             method: 'POST',
                             headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 'Content-Type': 'application/json' },
                             body: JSON.stringify({ amount: 10, motif: 'Comparaison de véhicules' })
                           });
                        } catch(e) {}
                        
                        navigate(`/compare?v1=${annonce.id}&v2=${similar.id}`);
                        setShowCompareModal(false);
                      }}
                      className="w-full flex items-center gap-6 p-6 bg-primary-elevated hover:bg-primary-card border border-primary-border/DEFAULT hover:border-accent rounded-[2rem] transition-all group relative overflow-hidden"
                    >
                      <div className="absolute -right-10 -bottom-10 w-32 h-32 bg-accent/5 rounded-full blur-2xl group-hover:bg-accent/10 transition-all" />
                      <div className="w-20 h-20 bg-black/30 rounded-2xl flex items-center justify-center text-4xl group-hover:scale-110 transition-all shadow-xl">
                        🚗
                      </div>
                      <div className="text-left flex-1 relative z-10">
                        <p className="font-black text-white text-lg tracking-tight group-hover:text-accent transition-colors">{similar.titre}</p>
                        <div className="flex items-center gap-3 mt-1">
                           <span className="text-accent font-bold">{similar.prix.toLocaleString()}€</span>
                           <span className="text-primary-text-secondary">•</span>
                           <span className="text-xs text-primary-text-secondary">{similar.kilometrage.toLocaleString()} km</span>
                        </div>
                      </div>
                      <div className="w-12 h-12 bg-white/5 group-hover:bg-accent rounded-xl flex items-center justify-center text-primary-text-secondary group-hover:text-white transition-all transform group-hover:rotate-12">
                         <Swords size={20} />
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="text-center py-16 opacity-50 italic">
                    Aucun adversaire digne n'a été trouvé.
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
