import React, { useState, useEffect } from 'react'
import { User, Mail, Phone, MapPin, Calendar, Settings, Bell, Heart, Shield, Star, Edit, Camera, ChevronRight } from 'lucide-react'

export default function Profil() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('annonces')
  const [editMode, setEditMode] = useState(false)

  useEffect(() => {
    fetchUserProfile()
  }, [])

  const fetchUserProfile = async () => {
    setLoading(true)
    try {
      // Simuler API call
      setTimeout(() => {
        setUser({
          id: 1,
          username: 'jean_dupont',
          email: 'jean.dupont@email.com',
          first_name: 'Jean',
          last_name: 'Dupont',
          phone: '06 12 34 56 78',
          avatar: '/images/avatars/user1.jpg',
          date_joined: '2024-01-15',
          last_login: '2024-01-18',
          is_premium: true,
          premium_expires: '2024-12-31',
          location: 'Paris, France',
          bio: 'Passionné d\'automobile, je recherche toujours les meilleures affaires sur le marché.',
          stats: {
            total_annonces_vues: 1234,
            alertes_actives: 5,
            estimations_realisees: 23,
            favorites_count: 12,
            bonnes_affaires_trouvees: 8
          },
          recent_activity: [
            {
              type: 'vue',
              titre: 'Peugeot 208 GT Line 2021',
              date: '2024-01-18',
              prix: 18500
            },
            {
              type: 'estimation',
              titre: 'Renault Clio E-Tech 2022',
              date: '2024-01-17',
              prix_estime: 23000
            },
            {
              type: 'favori',
              titre: 'BMW Série 3 2020',
              date: '2024-01-16',
              prix: 28900
            }
          ],
          favorites: [
            {
              id: 1,
              titre: 'Peugeot 208 GT Line 2021',
              prix: 18500,
              marque_nom: 'Peugeot',
              modele_nom: '208',
              ville: 'Paris',
              image: '/images/peugeot208-1.jpg',
              date_ajout: '2024-01-15'
            },
            {
              id: 2,
              titre: 'BMW Série 3 2020',
              prix: 28900,
              marque_nom: 'BMW',
              modele_nom: 'Série 3',
              ville: 'Lyon',
              image: '/images/bmw3-1.jpg',
              date_ajout: '2024-01-14'
            }
          ],
          alerts: [
            {
              id: 1,
              titre: 'Peugeot 208 - Prix max 20000€',
              criteres: {
                marque: 'Peugeot',
                modele: '208',
                prix_max: 20000,
                km_max: 50000
              },
              email_actif: true,
              push_actif: true,
              created_at: '2024-01-10',
              last_triggered: '2024-01-15'
            },
            {
              id: 2,
              titre: 'SUV Diesel - Occasion',
              criteres: {
                categorie: 'suv',
                carburant: 'diesel',
                annee_min: 2018
              },
              email_actif: true,
              push_actif: false,
              created_at: '2024-01-08',
              last_triggered: null
            }
          ]
        })
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching user profile:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse-slow">
            <div className="h-8 bg-primary-card rounded w-1/3 mb-8"></div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="h-96 bg-primary-card rounded-xl"></div>
              <div className="lg:col-span-2 h-96 bg-primary-card rounded-xl"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-primary-text-primary mb-4">Profil non trouvé</h1>
            <p className="text-primary-text-secondary">Veuillez vous connecter pour accéder à votre profil.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Mon Profil</h1>
          <p className="text-primary-text-secondary">Gérez vos informations et préférences</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Colonne profil */}
          <div className="space-y-6">
            {/* Carte profil */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-primary-text-primary">Informations</h2>
                <button
                  onClick={() => setEditMode(!editMode)}
                  className="p-2 border border-primary-border/DEFAULT rounded-lg hover:bg-primary-elevated transition-colors duration-200"
                >
                  <Edit className="w-4 h-4 text-primary-text-secondary" />
                </button>
              </div>
              
              <div className="text-center mb-6">
                <div className="relative inline-block">
                  <div className="w-24 h-24 bg-accent rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
                    {user.first_name[0]}{user.last_name[0]}
                  </div>
                  {editMode && (
                    <button className="absolute bottom-2 right-2 p-2 bg-accent text-white rounded-full hover:bg-accent-secondary transition-colors duration-200">
                      <Camera className="w-4 h-4" />
                    </button>
                  )}
                </div>
                
                <h3 className="text-xl font-bold text-primary-text-primary mb-1">
                  {user.first_name} {user.last_name}
                </h3>
                <p className="text-primary-text-secondary mb-2">@{user.username}</p>
                
                {/* Badge Premium */}
                {user.is_premium && (
                  <div className="inline-flex items-center space-x-1 bg-gradient-to-r from-accent to-accent-secondary text-white px-3 py-1 rounded-full text-sm font-bold">
                    <Star className="w-4 h-4" />
                    <span>Premium</span>
                  </div>
                )}
              </div>
              
              {/* Informations détaillées */}
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <Mail className="w-5 h-5 text-primary-text-secondary" />
                  <div>
                    <p className="text-sm text-primary-text-secondary">Email</p>
                    {editMode ? (
                      <input
                        type="email"
                        defaultValue={user.email}
                        className="bg-primary-elevated border border-primary-border/DEFAULT rounded px-2 py-1 text-primary-text-primary"
                      />
                    ) : (
                      <p className="text-primary-text-primary">{user.email}</p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Phone className="w-5 h-5 text-primary-text-secondary" />
                  <div>
                    <p className="text-sm text-primary-text-secondary">Téléphone</p>
                    {editMode ? (
                      <input
                        type="tel"
                        defaultValue={user.phone}
                        className="bg-primary-elevated border border-primary-border/DEFAULT rounded px-2 py-1 text-primary-text-primary"
                      />
                    ) : (
                      <p className="text-primary-text-primary">{user.phone}</p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <MapPin className="w-5 h-5 text-primary-text-secondary" />
                  <div>
                    <p className="text-sm text-primary-text-secondary">Localisation</p>
                    {editMode ? (
                      <input
                        type="text"
                        defaultValue={user.location}
                        className="bg-primary-elevated border border-primary-border/DEFAULT rounded px-2 py-1 text-primary-text-primary"
                      />
                    ) : (
                      <p className="text-primary-text-primary">{user.location}</p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Calendar className="w-5 h-5 text-primary-text-secondary" />
                  <div>
                    <p className="text-sm text-primary-text-secondary">Membre depuis</p>
                    <p className="text-primary-text-primary">{new Date(user.date_joined).toLocaleDateString('fr-FR')}</p>
                  </div>
                </div>
              </div>
              
              {editMode && (
                <div className="mt-6 flex space-x-2">
                  <button className="flex-1 bg-accent hover:bg-accent-secondary text-white py-2 rounded-lg font-medium transition-colors duration-200">
                    Sauvegarder
                  </button>
                  <button 
                    onClick={() => setEditMode(false)}
                    className="flex-1 bg-primary-elevated hover:bg-primary-elevated/90 text-primary-text-primary py-2 rounded-lg font-medium transition-colors duration-200"
                  >
                    Annuler
                  </button>
                </div>
              )}
            </div>

            {/* Statistiques */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
              <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Mes Statistiques</h3>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <p className="text-2xl font-bold text-primary-text-primary">{user.stats.total_annonces_vues}</p>
                  <p className="text-sm text-primary-text-secondary">Annonces vues</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-primary-text-primary">{user.stats.alertes_actives}</p>
                  <p className="text-sm text-primary-text-secondary">Alertes actives</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-primary-text-primary">{user.stats.estimations_realisees}</p>
                  <p className="text-sm text-primary-text-secondary">Estimations</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-primary-text-primary">{user.stats.favorites_count}</p>
                  <p className="text-sm text-primary-text-secondary">Favoris</p>
                </div>
              </div>
              
              <div className="mt-4 p-3 bg-success/10 rounded-lg">
                <div className="flex items-center space-x-2 text-success">
                  <Star className="w-5 h-5" />
                  <span className="font-medium">{user.stats.bonnes_affaires_trouvees} bonnes affaires trouvées</span>
                </div>
              </div>
            </div>
          </div>

          {/* Colonne contenu */}
          <div className="lg:col-span-2">
            {/* Onglets */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl">
              {/* Navigation des onglets */}
              <div className="flex border-b border-primary-border/DEFAULT">
                <button
                  onClick={() => setActiveTab('annonces')}
                  className={`flex-1 py-4 px-6 text-center font-medium transition-colors duration-200 ${
                    activeTab === 'annonces' 
                      ? 'text-accent border-b-2 border-accent' 
                      : 'text-primary-text-secondary hover:text-primary-text-primary'
                  }`}
                >
                  Annonces récentes
                </button>
                <button
                  onClick={() => setActiveTab('favoris')}
                  className={`flex-1 py-4 px-6 text-center font-medium transition-colors duration-200 ${
                    activeTab === 'favoris' 
                      ? 'text-accent border-b-2 border-accent' 
                      : 'text-primary-text-secondary hover:text-primary-text-primary'
                  }`}
                >
                  Favoris
                </button>
                <button
                  onClick={() => setActiveTab('alertes')}
                  className={`flex-1 py-4 px-6 text-center font-medium transition-colors duration-200 ${
                    activeTab === 'alertes' 
                      ? 'text-accent border-b-2 border-accent' 
                      : 'text-primary-text-secondary hover:text-primary-text-primary'
                  }`}
                >
                  Alertes
                </button>
              </div>

              {/* Contenu des onglets */}
              <div className="p-6">
                {activeTab === 'annonces' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Activité récente</h3>
                    {user.recent_activity.map((activity, index) => (
                      <div key={index} className="flex items-center space-x-4 p-4 bg-primary-elevated rounded-lg">
                        <div className={`p-2 rounded-lg ${
                          activity.type === 'vue' ? 'bg-blue-500/10 text-blue-500' :
                          activity.type === 'estimation' ? 'bg-green-500/10 text-green-500' :
                          'bg-red-500/10 text-red-500'
                        }`}>
                          {activity.type === 'vue' ? <Eye className="w-5 h-5" /> :
                           activity.type === 'estimation' ? <Settings className="w-5 h-5" /> :
                           <Heart className="w-5 h-5" />}
                        </div>
                        <div className="flex-1">
                          <p className="font-medium text-primary-text-primary">{activity.titre}</p>
                          <p className="text-sm text-primary-text-secondary">
                            {activity.type === 'vue' ? 'Vue le' :
                             activity.type === 'estimation' ? 'Estimée le' :
                             'Ajoutée aux favoris le'} {new Date(activity.date).toLocaleDateString('fr-FR')}
                          </p>
                        </div>
                        <div className="text-right">
                          {activity.prix && (
                            <p className="font-bold text-primary-text-primary">{activity.prix.toLocaleString()}€</p>
                          )}
                          {activity.prix_estime && (
                            <p className="font-bold text-accent">{activity.prix_estime.toLocaleString()}€</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'favoris' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Mes favoris</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {user.favorites.map((favorite) => (
                        <div key={favorite.id} className="bg-primary-elevated rounded-lg p-4 hover:bg-primary-elevated/90 transition-colors duration-200">
                          <div className="flex space-x-4">
                            <div className="w-20 h-20 bg-primary-card rounded-lg flex items-center justify-center">
                              <div className="text-3xl text-primary-text-secondary">🚗</div>
                            </div>
                            <div className="flex-1">
                              <h4 className="font-medium text-primary-text-primary mb-1">{favorite.titre}</h4>
                              <p className="text-sm text-primary-text-secondary mb-2">
                                {favorite.marque_nom} {favorite.modele_nom} • {favorite.ville}
                              </p>
                              <div className="flex items-center justify-between">
                                <span className="text-lg font-bold text-primary-text-primary">{favorite.prix.toLocaleString()}€</span>
                                <button className="text-red-500 hover:text-red-600 transition-colors duration-200">
                                  <Heart className="w-5 h-5 fill-current" />
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'alertes' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Mes alertes</h3>
                    {user.alerts.map((alert) => (
                      <div key={alert.id} className="bg-primary-elevated rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-medium text-primary-text-primary">{alert.titre}</h4>
                          <div className="flex items-center space-x-2">
                            <button className={`p-2 rounded-lg ${
                              alert.email_actif ? 'bg-success/10 text-success' : 'bg-primary-border/DEFAULT text-primary-text-secondary'
                            }`}>
                              <Mail className="w-4 h-4" />
                            </button>
                            <button className={`p-2 rounded-lg ${
                              alert.push_actif ? 'bg-success/10 text-success' : 'bg-primary-border/DEFAULT text-primary-text-secondary'
                            }`}>
                              <Bell className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 text-sm text-primary-text-secondary mb-3">
                          {Object.entries(alert.criteres).map(([key, value]) => (
                            <div key={key}>
                              <span className="font-medium capitalize">{key}:</span> {value}
                            </div>
                          ))}
                        </div>
                        
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-primary-text-secondary">
                            Créée le {new Date(alert.created_at).toLocaleDateString('fr-FR')}
                          </span>
                          {alert.last_triggered && (
                            <span className="text-primary-text-secondary">
                              Dernière notification: {new Date(alert.last_triggered).toLocaleDateString('fr-FR')}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
