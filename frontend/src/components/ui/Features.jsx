import React from 'react'

export default function Features() {
  return (
    <section id="fonctionnalites" className="py-20">
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-12">Fonctionnalités principales</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-8 card-hover">
            <div className="text-purple-600 text-4xl mb-4">
              <i className="fas fa-robot"></i>
            </div>
            <h3 className="text-xl font-bold mb-4">Estimation par IA</h3>
            <p className="text-gray-600">
              Notre algorithme de machine learning analyse des milliers d'annonces pour vous donner une estimation précise de votre véhicule.
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8 card-hover">
            <div className="text-purple-600 text-4xl mb-4">
              <i className="fas fa-search"></i>
            </div>
            <h3 className="text-xl font-bold mb-4">Scraping Intelligent</h3>
            <p className="text-gray-600">
              Collecte automatique des annonces des principales plateformes pour une analyse en temps réel du marché.
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8 card-hover">
            <div className="text-purple-600 text-4xl mb-4">
              <i className="fas fa-chart-line"></i>
            </div>
            <h3 className="text-xl font-bold mb-4">Dashboard Analytique</h3>
            <p className="text-gray-600">
              Visualisez les tendances du marché, les prix moyens et les meilleures opportunités d'achat.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
