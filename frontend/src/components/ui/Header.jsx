import React from 'react'

export default function Header() {
  return (
    <header className="gradient-bg text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <i className="fas fa-car text-3xl"></i>
            <h1 className="text-2xl font-bold">AutoIntel</h1>
          </div>
          <nav className="hidden md:flex space-x-6">
            <a href="#accueil" className="hover:text-purple-200 transition">Accueil</a>
            <a href="#fonctionnalites" className="hover:text-purple-200 transition">Fonctionnalités</a>
            <a href="#estimation" className="hover:text-purple-200 transition">Estimation</a>
            <a href="#dashboard" className="hover:text-purple-200 transition">Dashboard</a>
          </nav>
          <button className="bg-white text-purple-600 px-4 py-2 rounded-lg font-semibold hover:bg-purple-50 transition">
            Connexion
          </button>
        </div>
      </div>
    </header>
  )
}
