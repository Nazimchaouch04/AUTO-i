import React from 'react'

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <i className="fas fa-car text-2xl"></i>
              <h3 className="text-xl font-bold">AutoIntel</h3>
            </div>
            <p className="text-gray-400">
              L'intelligence artificielle au service de l'automobile.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Produit</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition">Estimation</a></li>
              <li><a href="#" className="hover:text-white transition">Dashboard</a></li>
              <li><a href="#" className="hover:text-white transition">Alertes</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Ressources</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition">Documentation</a></li>
              <li><a href="#" className="hover:text-white transition">API</a></li>
              <li><a href="#" className="hover:text-white transition">Blog</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Contact</h4>
            <ul className="space-y-2 text-gray-400">
              <li><i className="fas fa-envelope mr-2"></i>contact@autointel.fr</li>
              <li><i className="fas fa-phone mr-2"></i>+33 1 234 567 890</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 AutoIntel. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  )
}
