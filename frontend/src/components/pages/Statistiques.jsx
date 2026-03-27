import React, { useState, useEffect } from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, TrendingDown, BarChart3, PieChart as PieChartIcon, Activity, Calendar, DollarSign, Car, Eye, Download, Filter } from 'lucide-react'

export default function Statistiques() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedPeriod, setSelectedPeriod] = useState('30j')
  const [selectedChart, setSelectedChart] = useState('prix')

  useEffect(() => {
    fetchStatistics()
  }, [selectedPeriod])

  const fetchStatistics = async () => {
    setLoading(true)
    try {
      // Simuler API call
      setTimeout(() => {
        setStats({
          overview: {
            total_annonces: 12453,
            nouvelles_annonces: 234,
            prix_moyen: 15234,
            prix_median: 14500,
            bonnes_affaires: 147,
            taux_bonnes_affaires: 1.2,
            marques_count: 45,
            modeles_count: 234
          },
          evolutionPrix: [
            { mois: 'Jan', prix_moyen: 14200, prix_median: 13500, volume: 890 },
            { mois: 'Fév', prix_moyen: 14800, prix_median: 14100, volume: 920 },
            { mois: 'Mar', prix_moyen: 15100, prix_median: 14500, volume: 980 },
            { mois: 'Avr', prix_moyen: 14900, prix_median: 14300, volume: 1050 },
            { mois: 'Mai', prix_moyen: 15300, prix_median: 14800, volume: 1120 },
            { mois: 'Juin', prix_moyen: 15700, prix_median: 15200, volume: 1180 }
          ],
          repartitionMarques: [
            { marque: 'Peugeot', count: 2341, prix_moyen: 14500, pourcentage: 18.8 },
            { marque: 'Renault', count: 2156, prix_moyen: 13800, pourcentage: 17.3 },
            { marque: 'Volkswagen', count: 1987, prix_moyen: 18200, pourcentage: 16.0 },
            { marque: 'Toyota', count: 1432, prix_moyen: 17800, pourcentage: 11.5 },
            { marque: 'Ford', count: 1543, prix_moyen: 16500, pourcentage: 12.4 },
            { marque: 'BMW', count: 1234, prix_moyen: 24800, pourcentage: 9.9 },
            { marque: 'Mercedes', count: 987, prix_moyen: 26500, pourcentage: 7.9 },
            { marque: 'Audi', count: 876, prix_moyen: 24000, pourcentage: 7.0 }
          ],
          repartitionCarburants: [
            { nom: 'Essence', valeur: 45, color: '#6C63FF' },
            { nom: 'Diesel', valeur: 32, color: '#00D4AA' },
            { nom: 'Électrique', valeur: 18, color: '#F59E0B' },
            { nom: 'Hybride', valeur: 5, color: '#EF4444' }
          ],
          repartitionCategories: [
            { categorie: 'Citadine', count: 3456, pourcentage: 27.7 },
            { categorie: 'Berline', count: 4123, pourcentage: 33.1 },
            { categorie: 'SUV', count: 2876, pourcentage: 23.1 },
            { categorie: 'Compact', count: 1234, pourcentage: 9.9 },
            { categorie: 'Monospace', count: 543, pourcentage: 4.4 },
            { categorie: 'Utilitaire', count: 221, pourcentage: 1.8 }
          ],
          tendances: {
            prix_moyen_evolution: 10.3,
            volume_evolution: 32.5,
            bonnes_affaires_evolution: -5.2,
            marques_populaires: ['Peugeot', 'Renault', 'Volkswagen'],
            modeles_tendance: ['Peugeot 208', 'Renault Clio', 'Volkswagen Golf']
          }
        })
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching statistics:', error)
      setLoading(false)
    }
  }

  const COLORS = ['#6C63FF', '#00D4AA', '#F59E0B', '#EF4444']

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse-slow">
            <div className="h-8 bg-primary-card rounded w-1/3 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              {[...Array(4)].map((_, index) => (
                <div key={index} className="h-32 bg-primary-card rounded-xl"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="h-96 bg-primary-card rounded-xl"></div>
              <div className="h-96 bg-primary-card rounded-xl"></div>
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
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 space-y-4 sm:space-y-0 sm:space-x-4">
          <div>
            <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Statistiques du marché</h1>
            <p className="text-primary-text-secondary">Analyse complète du marché automobile</p>
          </div>
          
          {/* Filtres */}
          <div className="flex items-center space-x-2">
            <span className="text-primary-text-secondary text-sm">Période:</span>
            {['7j', '30j', '90j', '1an'].map((period) => (
              <button
                key={period}
                onClick={() => setSelectedPeriod(period)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  selectedPeriod === period
                    ? 'bg-accent text-white'
                    : 'bg-primary-card text-primary-text-secondary hover:bg-primary-elevated'
                }`}
              >
                {period}
              </button>
            ))}
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-lg bg-accent/10">
                <Car className="w-6 h-6 text-accent" />
              </div>
              <div className="flex items-center space-x-1 text-success">
                <TrendingUp className="w-4 h-4" />
                <span className="text-sm font-medium">+12%</span>
              </div>
            </div>
            <h3 className="text-primary-text-secondary text-sm font-medium mb-1">Total annonces</h3>
            <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.total_annonces.toLocaleString()}</p>
            <p className="text-sm text-primary-text-secondary mt-2">{stats.overview.nouvelles_annonces} nouvelles aujourd'hui</p>
          </div>

          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-lg bg-accent-secondary/10">
                <DollarSign className="w-6 h-6 text-accent-secondary" />
              </div>
              <div className="flex items-center space-x-1 text-success">
                <TrendingUp className="w-4 h-4" />
                <span className="text-sm font-medium">+8.3%</span>
              </div>
            </div>
            <h3 className="text-primary-text-secondary text-sm font-medium mb-1">Prix moyen</h3>
            <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.prix_moyen.toLocaleString()}€</p>
            <p className="text-sm text-primary-text-secondary mt-2">Médiane: {stats.overview.prix_median.toLocaleString()}€</p>
          </div>

          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-lg bg-success/10">
                <Activity className="w-6 h-6 text-success" />
              </div>
              <div className="flex items-center space-x-1 text-danger">
                <TrendingDown className="w-4 h-4" />
                <span className="text-sm font-medium">-5.2%</span>
              </div>
            </div>
            <h3 className="text-primary-text-secondary text-sm font-medium mb-1">Bonnes affaires</h3>
            <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.bonnes_affaires}</p>
            <p className="text-sm text-primary-text-secondary mt-2">{stats.overview.taux_bonnes_affaires}% du marché</p>
          </div>

          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-lg bg-warning/10">
                <BarChart3 className="w-6 h-6 text-warning" />
              </div>
              <div className="flex items-center space-x-1 text-success">
                <TrendingUp className="w-4 h-4" />
                <span className="text-sm font-medium">+15%</span>
              </div>
            </div>
            <h3 className="text-primary-text-secondary text-sm font-medium mb-1">Marques</h3>
            <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.marques_count}</p>
            <p className="text-sm text-primary-text-secondary mt-2">{stats.overview.modeles_count} modèles</p>
          </div>
        </div>

        {/* Graphiques */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Évolution des prix */}
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-primary-text-primary">Évolution des prix</h3>
              <div className="flex items-center space-x-2">
                <Activity className="w-5 h-5 text-primary-text-secondary" />
                <span className="text-sm text-primary-text-secondary">6 derniers mois</span>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={stats.evolutionPrix}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A3E" />
                <XAxis dataKey="mois" stroke="#8B8BA0" />
                <YAxis stroke="#8B8BA0" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1C1C2E', border: '1px solid #2A2A3E' }}
                  labelStyle={{ color: '#F0F0F5' }}
                />
                <Legend />
                <Line type="monotone" dataKey="prix_moyen" stroke="#6C63FF" strokeWidth={2} name="Prix moyen" />
                <Line type="monotone" dataKey="prix_median" stroke="#00D4AA" strokeWidth={2} name="Prix médian" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Répartition par carburant */}
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-primary-text-primary">Répartition par carburant</h3>
              <div className="flex items-center space-x-2">
                <PieChartIcon className="w-5 h-5 text-primary-text-secondary" />
                <span className="text-sm text-primary-text-secondary">Marché actuel</span>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.repartitionCarburants}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ nom, valeur }) => `${nom}: ${valeur}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="valeur"
                >
                  {stats.repartitionCarburants.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top marques */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-primary-text-primary">Top marques</h3>
            <div className="flex items-center space-x-2">
              <Car className="w-5 h-5 text-primary-text-secondary" />
              <span className="text-sm text-primary-text-secondary">Par nombre d'annonces</span>
            </div>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats.repartitionMarques}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2A2A3E" />
                  <XAxis dataKey="marque" stroke="#8B8BA0" />
                  <YAxis stroke="#8B8BA0" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1C1C2E', border: '1px solid #2A2A3E' }}
                    labelStyle={{ color: '#F0F0F5' }}
                  />
                  <Bar dataKey="count" fill="#6C63FF" name="Annonces" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div>
              <div className="space-y-3">
                {stats.repartitionMarques.slice(0, 5).map((marque, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-primary-elevated rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center text-white text-sm font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <p className="font-medium text-primary-text-primary">{marque.marque}</p>
                        <p className="text-sm text-primary-text-secondary">{marque.count} annonces</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-primary-text-primary">{marque.prix_moyen.toLocaleString()}€</p>
                      <p className="text-sm text-primary-text-secondary">{marque.pourcentage}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Répartition par catégorie */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-primary-text-primary">Répartition par catégorie</h3>
            <div className="flex items-center space-x-2">
              <Filter className="w-5 h-5 text-primary-text-secondary" />
              <span className="text-sm text-primary-text-secondary">Toutes catégories</span>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {stats.repartitionCategories.map((categorie, index) => (
              <div key={index} className="bg-primary-elevated rounded-lg p-4 text-center">
                <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center text-accent font-bold mx-auto mb-2">
                  {index + 1}
                </div>
                <p className="font-medium text-primary-text-primary mb-1">{categorie.categorie}</p>
                <p className="text-lg font-bold text-primary-text-primary">{categorie.count}</p>
                <p className="text-sm text-primary-text-secondary">{categorie.pourcentage}%</p>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-center space-x-4 mt-8">
          <button className="flex items-center space-x-2 bg-accent hover:bg-accent-secondary text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200">
            <Download className="w-5 h-5" />
            <span>Exporter les données</span>
          </button>
          <button className="flex items-center space-x-2 bg-primary-elevated hover:bg-primary-elevated/90 text-primary-text-primary px-6 py-3 rounded-lg font-medium transition-colors duration-200">
            <Calendar className="w-5 h-5" />
            <span>Planifier un rapport</span>
          </button>
        </div>
      </div>
    </div>
  )
}
