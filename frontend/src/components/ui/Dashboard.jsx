import React from 'react'

export default function Dashboard() {
  return (
    <section id="dashboard" className="py-20">
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-12">Dashboard Analytique</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-600">Annonces analysées</h3>
              <i className="fas fa-car text-purple-600 text-2xl"></i>
            </div>
            <p className="text-3xl font-bold">12,453</p>
            <p className="text-green-600 text-sm">+12% ce mois</p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-600">Estimations réalisées</h3>
              <i className="fas fa-chart-line text-purple-600 text-2xl"></i>
            </div>
            <p className="text-3xl font-bold">3,892</p>
            <p className="text-green-600 text-sm">+8% ce mois</p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-600">Bonnes affaires</h3>
              <i className="fas fa-tag text-purple-600 text-2xl"></i>
            </div>
            <p className="text-3xl font-bold">147</p>
            <p className="text-green-600 text-sm">+23% ce mois</p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-600">Utilisateurs actifs</h3>
              <i className="fas fa-users text-purple-600 text-2xl"></i>
            </div>
            <p className="text-3xl font-bold">892</p>
            <p className="text-green-600 text-sm">+15% ce mois</p>
          </div>
        </div>
        
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-bold mb-6">Évolution des prix</h3>
            <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
              <i className="fas fa-chart-area text-6xl text-gray-400"></i>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-bold mb-6">Répartition par marque</h3>
            <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
              <i className="fas fa-chart-pie text-6xl text-gray-400"></i>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
