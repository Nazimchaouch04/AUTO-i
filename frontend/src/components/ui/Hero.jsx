import React from 'react'

export default function Hero() {
  return (
    <section id="accueil" className="gradient-bg text-white py-20">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-5xl font-bold mb-6">L'intelligence artificielle au service de l'automobile</h2>
        <p className="text-xl mb-8 max-w-2xl mx-auto">
          Estimez le prix de votre véhicule avec précision, détectez les bonnes affaires et analysez les tendances du marché automobile.
        </p>
        <div className="space-x-4">
          <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-purple-50 transition">
            Commencer gratuitement
          </button>
          <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition">
            Voir la démo
          </button>
        </div>
      </div>
    </section>
  )
}
