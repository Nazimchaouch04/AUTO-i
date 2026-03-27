import React, { useState, useEffect } from 'react'
import { Bell, Plus, Search, Filter, Mail, Smartphone, Calendar, Settings, Trash2, Edit, Eye } from 'lucide-react'

export default function Alertes() {
  const [alertes, setAlertes] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingAlert, setEditingAlert] = useState(null)
  const [formData, setFormData] = useState({
    titre: '',
    marque: '',
    modele: '',
    prix_min: '',
    prix_max: '',
    km_max: '',
    annee_min: '',
    carburant: '',
    boite_vitesse: '',
    departement: '',
    email_actif: true,
    push_actif: true
  })

  useEffect(() => {
    fetchAlertes()
  }, [])

  const fetchAlertes = async () => {
    setLoading(true)
    try {
      // Simuler API call
      setTimeout(() => {
        setAlertes([
          {
            id: 1,
            titre: 'Peugeot 208 - Prix max 20000€',
            criteres: {
              marque: 'Peugeot',
              modele: '208',
              prix_max: 20000,
              km_max: 50000,
              annee_min: 2020
            },
            email_actif: true,
            push_actif: true,
            created_at: '2024-01-10',
            last_triggered: '2024-01-15',
            nombre_alertes: 3,
            dernieres_annonces: [
              { titre: 'Peugeot 208 GT Line 2021', prix: 18500, date: '2024-01-15' },
              { titre: 'Peugeot 208 Active 2020', prix: 16900, date: '2024-01-14' },
              { titre: 'Peugeot 208 Allure 2022', prix: 19500, date: '2024-01-13' }
            ]
          },
          {
            id: 2,
            titre: 'SUV Diesel - Occasion',
            criteres: {
              categorie: 'suv',
              carburant: 'diesel',
              annee_min: 2018,
              prix_max: 30000
            },
            email_actif: true,
            push_actif: false,
            created_at: '2024-01-08',
            last_triggered: '2024-01-12',
            nombre_alertes: 5,
            dernieres_annonces: [
              { titre: 'Renault Captur 1.5 Blue dCi 2019', prix: 18900, date: '2024-01-12' },
              { titre: 'Peugeot 2008 1.5 BlueHDi 2020', prix: 21000, date: '2024-01-11' }
            ]
          },
          {
            id: 3,
            titre: 'BMW Série 3 - Budget 30k€',
            criteres: {
              marque: 'BMW',
              modele: 'Série 3',
              prix_max: 30000,
              annee_min: 2018,
              km_max: 80000
            },
            email_actif: false,
            push_actif: true,
            created_at: '2024-01-05',
            last_triggered: '2024-01-10',
            nombre_alertes: 2,
            dernieres_annonces: [
              { titre: 'BMW 320i 2019', prix: 28900, date: '2024-01-10' }
            ]
          }
        ])
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching alertes:', error)
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (editingAlert) {
      // Mise à jour d'une alerte existante
      setAlertes(prev => prev.map(alert => 
        alert.id === editingAlert.id 
          ? { ...alert, ...formData, criteres: getCriteresFromForm() }
          : alert
      ))
    } else {
      // Création d'une nouvelle alerte
      const newAlert = {
        id: Date.now(),
        titre: formData.titre,
        criteres: getCriteresFromForm(),
        email_actif: formData.email_actif,
        push_actif: formData.push_actif,
        created_at: new Date().toISOString().split('T')[0],
        last_triggered: null,
        nombre_alertes: 0,
        dernieres_annonces: []
      }
      setAlertes(prev => [...prev, newAlert])
    }
    
    resetForm()
  }

  const getCriteresFromForm = () => {
    const criteres = {}
    if (formData.marque) criteres.marque = formData.marque
    if (formData.modele) criteres.modele = formData.modele
    if (formData.prix_min) criteres.prix_min = parseInt(formData.prix_min)
    if (formData.prix_max) criteres.prix_max = parseInt(formData.prix_max)
    if (formData.km_max) criteres.km_max = parseInt(formData.km_max)
    if (formData.annee_min) criteres.annee_min = parseInt(formData.annee_min)
    if (formData.carburant) criteres.carburant = formData.carburant
    if (formData.boite_vitesse) criteres.boite_vitesse = formData.boite_vitesse
    if (formData.departement) criteres.departement = formData.departement
    return criteres
  }

  const handleEdit = (alert) => {
    setEditingAlert(alert)
    setFormData({
      titre: alert.titre,
      marque: alert.criteres.marque || '',
      modele: alert.criteres.modele || '',
      prix_min: alert.criteres.prix_min || '',
      prix_max: alert.criteres.prix_max || '',
      km_max: alert.criteres.km_max || '',
      annee_min: alert.criteres.annee_min || '',
      carburant: alert.criteres.carburant || '',
      boite_vitesse: alert.criteres.boite_vitesse || '',
      departement: alert.criteres.departement || '',
      email_actif: alert.email_actif,
      push_actif: alert.push_actif
    })
    setShowForm(true)
  }

  const handleDelete = (id) => {
    setAlertes(prev => prev.filter(alert => alert.id !== id))
  }

  const resetForm = () => {
    setFormData({
      titre: '',
      marque: '',
      modele: '',
      prix_min: '',
      prix_max: '',
      km_max: '',
      annee_min: '',
      carburant: '',
      boite_vitesse: '',
      departement: '',
      email_actif: true,
      push_actif: true
    })
    setEditingAlert(null)
    setShowForm(false)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse-slow">
            <div className="h-8 bg-primary-card rounded w-1/3 mb-8"></div>
            <div className="space-y-4">
              {[...Array(3)].map((_, index) => (
                <div key={index} className="h-32 bg-primary-card rounded-xl"></div>
              ))}
            </div>
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
          <div>
            <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Mes Alertes</h1>
            <p className="text-primary-text-secondary">Soyez notifié des nouvelles annonces correspondant à vos critères</p>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center space-x-2 bg-accent hover:bg-accent-secondary text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            <Plus className="w-5 h-5" />
            <span>Nouvelle alerte</span>
          </button>
        </div>

        {/* Formulaire d'alerte */}
        {showForm && (
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-primary-text-primary">
                {editingAlert ? 'Modifier l\'alerte' : 'Créer une nouvelle alerte'}
              </h2>
              <button
                onClick={resetForm}
                className="p-2 border border-primary-border/DEFAULT rounded-lg hover:bg-primary-elevated transition-colors duration-200"
              >
                <Trash2 className="w-4 h-4 text-primary-text-secondary" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-primary-text-secondary mb-2">Titre de l'alerte</label>
                <input
                  type="text"
                  required
                  value={formData.titre}
                  onChange={(e) => setFormData(prev => ({ ...prev, titre: e.target.value }))}
                  placeholder="Ex: Peugeot 208 - Prix max 20000€"
                  className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Marque</label>
                  <input
                    type="text"
                    value={formData.marque}
                    onChange={(e) => setFormData(prev => ({ ...prev, marque: e.target.value }))}
                    placeholder="Ex: Peugeot"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Modèle</label>
                  <input
                    type="text"
                    value={formData.modele}
                    onChange={(e) => setFormData(prev => ({ ...prev, modele: e.target.value }))}
                    placeholder="Ex: 208"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Carburant</label>
                  <select
                    value={formData.carburant}
                    onChange={(e) => setFormData(prev => ({ ...prev, carburant: e.target.value }))}
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
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Prix min</label>
                  <input
                    type="number"
                    value={formData.prix_min}
                    onChange={(e) => setFormData(prev => ({ ...prev, prix_min: e.target.value }))}
                    placeholder="0€"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Prix max</label>
                  <input
                    type="number"
                    value={formData.prix_max}
                    onChange={(e) => setFormData(prev => ({ ...prev, prix_max: e.target.value }))}
                    placeholder="50000€"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Kilométrage max</label>
                  <input
                    type="number"
                    value={formData.km_max}
                    onChange={(e) => setFormData(prev => ({ ...prev, km_max: e.target.value }))}
                    placeholder="100000 km"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Année min</label>
                  <input
                    type="number"
                    value={formData.annee_min}
                    onChange={(e) => setFormData(prev => ({ ...prev, annee_min: e.target.value }))}
                    placeholder="2018"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Boîte de vitesse</label>
                  <select
                    value={formData.boite_vitesse}
                    onChange={(e) => setFormData(prev => ({ ...prev, boite_vitesse: e.target.value }))}
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary focus:outline-none focus:border-accent"
                  >
                    <option value="">Toutes</option>
                    <option value="manuelle">Manuelle</option>
                    <option value="automatique">Automatique</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-primary-text-secondary mb-2">Département</label>
                  <input
                    type="text"
                    value={formData.departement}
                    onChange={(e) => setFormData(prev => ({ ...prev, departement: e.target.value }))}
                    placeholder="75"
                    className="w-full px-4 py-2 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg text-primary-text-primary placeholder-primary-text-secondary focus:outline-none focus:border-accent"
                  />
                </div>
              </div>
              
              <div className="flex items-center space-x-6">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.email_actif}
                    onChange={(e) => setFormData(prev => ({ ...prev, email_actif: e.target.checked }))}
                    className="w-4 h-4 text-accent bg-primary-elevated border-primary-border/DEFAULT rounded focus:ring-accent"
                  />
                  <span className="text-primary-text-primary">Notifications email</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.push_actif}
                    onChange={(e) => setFormData(prev => ({ ...prev, push_actif: e.target.checked }))}
                    className="w-4 h-4 text-accent bg-primary-elevated border-primary-border/DEFAULT rounded focus:ring-accent"
                  />
                  <span className="text-primary-text-primary">Notifications push</span>
                </label>
              </div>
              
              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="flex-1 bg-accent hover:bg-accent-secondary text-white py-3 rounded-lg font-medium transition-colors duration-200"
                >
                  {editingAlert ? 'Mettre à jour' : 'Créer l\'alerte'}
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="flex-1 bg-primary-elevated hover:bg-primary-elevated/90 text-primary-text-primary py-3 rounded-lg font-medium transition-colors duration-200"
                >
                  Annuler
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Liste des alertes */}
        <div className="space-y-6">
          {alertes.length === 0 ? (
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-12 text-center">
              <Bell className="w-16 h-16 text-primary-text-secondary mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-primary-text-primary mb-2">Aucune alerte</h3>
              <p className="text-primary-text-secondary mb-6">Créez votre première alerte pour être notifié des nouvelles annonces</p>
              <button
                onClick={() => setShowForm(true)}
                className="bg-accent hover:bg-accent-secondary text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
              >
                Créer une alerte
              </button>
            </div>
          ) : (
            alertes.map((alerte) => (
              <div key={alerte.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-primary-text-primary mb-2">{alerte.titre}</h3>
                    <p className="text-primary-text-secondary">
                      Créée le {new Date(alerte.created_at).toLocaleDateString('fr-FR')}
                      {alerte.last_triggered && (
                        <span> • Dernière notification le {new Date(alerte.last_triggered).toLocaleDateString('fr-FR')}</span>
                      )}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button className={`p-2 rounded-lg ${
                      alerte.email_actif ? 'bg-success/10 text-success' : 'bg-primary-border/DEFAULT text-primary-text-secondary'
                    }`}>
                      <Mail className="w-4 h-4" />
                    </button>
                    <button className={`p-2 rounded-lg ${
                      alerte.push_actif ? 'bg-success/10 text-success' : 'bg-primary-border/DEFAULT text-primary-text-secondary'
                    }`}>
                      <Smartphone className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleEdit(alerte)}
                      className="p-2 border border-primary-border/DEFAULT rounded-lg hover:bg-primary-elevated transition-colors duration-200"
                    >
                      <Edit className="w-4 h-4 text-primary-text-secondary" />
                    </button>
                    <button
                      onClick={() => handleDelete(alerte.id)}
                      className="p-2 border border-danger/DEFAULT rounded-lg hover:bg-danger/10 transition-colors duration-200"
                    >
                      <Trash2 className="w-4 h-4 text-danger" />
                    </button>
                  </div>
                </div>
                
                {/* Critères */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  {Object.entries(alerte.criteres).map(([key, value]) => (
                    <div key={key} className="bg-primary-elevated rounded-lg p-3">
                      <p className="text-xs text-primary-text-secondary capitalize">{key}</p>
                      <p className="font-medium text-primary-text-primary">{value}</p>
                    </div>
                  ))}
                </div>
                
                {/* Statistiques */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-primary-text-secondary">
                      <span className="font-bold text-primary-text-primary">{alerte.nombre_alertes}</span> annonces trouvées
                    </span>
                    {alerte.nombre_alertes > 0 && (
                      <span className="text-sm text-success">
                        {alerte.dernieres_annonces[0] && `Dernière: ${new Date(alerte.dernieres_annonces[0].date).toLocaleDateString('fr-FR')}`}
                      </span>
                    )}
                  </div>
                </div>
                
                {/* Dernières annonces */}
                {alerte.dernieres_annonces.length > 0 && (
                  <div className="border-t border-primary-border/DEFAULT pt-4">
                    <h4 className="text-sm font-medium text-primary-text-primary mb-3">Dernières annonces trouvées</h4>
                    <div className="space-y-2">
                      {alerte.dernieres_annonces.slice(0, 3).map((annonce, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-primary-elevated rounded-lg">
                          <div>
                            <p className="font-medium text-primary-text-primary">{annonce.titre}</p>
                            <p className="text-sm text-primary-text-secondary">{new Date(annonce.date).toLocaleDateString('fr-FR')}</p>
                          </div>
                          <div className="text-right">
                            <p className="font-bold text-accent">{annonce.prix.toLocaleString()}€</p>
                            <button className="text-sm text-primary-text-secondary hover:text-accent transition-colors duration-200">
                              Voir →
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
