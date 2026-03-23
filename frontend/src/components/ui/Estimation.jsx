import React, { useState } from 'react'

export default function Estimation() {
  const [formData, setFormData] = useState({
    marque: 'Peugeot',
    modele: '',
    annee: '',
    kilometrage: '',
    carburant: 'Essence',
    boite: 'Manuelle'
  })
  const [showResult, setShowResult] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    setShowResult(true)
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <section id="estimation" className="py-20 bg-gray-100">
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-12">Estimez votre véhicule</h2>
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Marque</label>
                <select 
                  name="marque"
                  value={formData.marque}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                >
                  <option>Peugeot</option>
                  <option>Renault</option>
                  <option>Volkswagen</option>
                  <option>BMW</option>
                  <option>Mercedes</option>
                  <option>Audi</option>
                </select>
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Modèle</label>
                <input 
                  type="text" 
                  name="modele"
                  placeholder="ex: 208, Clio, Golf" 
                  value={formData.modele}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Année</label>
                <input 
                  type="number" 
                  name="annee"
                  placeholder="ex: 2020" 
                  min="2000" 
                  max="2024"
                  value={formData.annee}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Kilométrage</label>
                <input 
                  type="number" 
                  name="kilometrage"
                  placeholder="ex: 50000"
                  value={formData.kilometrage}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Carburant</label>
                <select 
                  name="carburant"
                  value={formData.carburant}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                >
                  <option>Essence</option>
                  <option>Diesel</option>
                  <option>Électrique</option>
                  <option>Hybride</option>
                  <option>GPL</option>
                </select>
              </div>
              <div>
                <label className="block text-gray-700 font-semibold mb-2">Boîte de vitesse</label>
                <select 
                  name="boite"
                  value={formData.boite}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                >
                  <option>Manuelle</option>
                  <option>Automatique</option>
                  <option>Séquentielle</option>
                </select>
              </div>
            </div>
            <button type="submit" className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition">
              Estimer le prix
            </button>
          </form>
          {showResult && (
            <div className="mt-8 p-6 bg-purple-50 rounded-lg">
              <h3 className="text-xl font-bold text-purple-800 mb-4">Résultat de l'estimation</h3>
              <div className="grid md:grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-gray-600">Prix estimé</p>
                  <p className="text-2xl font-bold text-purple-600">15 000 €</p>
                </div>
                <div>
                  <p className="text-gray-600">Fourchette basse</p>
                  <p className="text-xl font-semibold">12 750 €</p>
                </div>
                <div>
                  <p className="text-gray-600">Fourchette haute</p>
                  <p className="text-xl font-semibold">17 250 €</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
