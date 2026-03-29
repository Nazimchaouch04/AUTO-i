import React, { useState } from 'react'
import { Bell, Search, Menu, X, TrendingUp, Users, Car, Settings, LogOut, Home, BarChart3, PieChart, Tag, Target, ChevronDown, User, Shield, Star, ArrowRight } from 'lucide-react'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [notifications, setNotifications] = useState(3)

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 bg-primary-bg/95 backdrop-blur-lg border-b border-primary-border/DEFAULT">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo + Menu Toggle */}
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="p-2 text-primary-text-secondary hover:text-white transition-colors duration-200 lg:hidden"
              >
                {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
              
              <div className="relative">
                <div className="absolute inset-0 bg-accent rounded-lg p-1">
                  <Car className="w-5 h-5 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-success rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-bold">AI</span>
                </div>
              </div>
              <h1 className="text-xl font-bold text-primary-text-primary hidden sm:block">AutoIntel</h1>
            </div>

            {/* Navigation Desktop */}
            <nav className="hidden lg:flex items-center space-x-6">
              <a href="#accueil" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <Home className="w-4 h-4" />
                <span>Accueil</span>
              </a>
              <a href="#marche" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>Marche</span>
              </a>
              <a href="#estimation" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <Target className="w-4 h-4" />
                <span>Estimation</span>
              </a>
              <a href="#dashboard" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <BarChart3 className="w-4 h-4" />
                <span>Dashboard</span>
              </a>
            </nav>

            {/* Actions */}
            <div className="flex items-center space-x-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-primary-text-secondary" />
                <input 
                  type="text" 
                  placeholder="Rechercher..." 
                  className="bg-primary-card border border-primary-border/DEFAULT rounded-lg pl-10 pr-4 py-2 text-primary-text-primary placeholder:text-primary-text-secondary focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 w-64 transition-all duration-200"
                />
              </div>

              {/* Notifications */}
              <div className="relative">
                <button className="relative p-2 text-primary-text-secondary hover:text-white transition-colors duration-200">
                  <Bell className="w-5 h-5" />
                  {notifications > 0 && (
                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-danger rounded-full flex items-center justify-center animate-pulse-slow">
                      <span className="text-white text-xs font-bold">{notifications}</span>
                    </span>
                  )}
                </button>
              </div>

              {/* User Menu */}
              <div className="relative">
                <button 
                  onClick={() => setIsMenuOpen(!isMenuOpen)}
                  className="flex items-center space-x-3 bg-primary-card border border-primary-border/DEFAULT rounded-lg px-4 py-2 text-primary-text-primary hover:bg-primary-elevated transition-all duration-200"
                >
                  <div className="w-8 h-8 bg-gradient-to-r from-accent to-accent-secondary rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex flex-col items-start">
                    <span className="text-sm font-medium text-primary-text-primary">Jean Dupont</span>
                    <div className="flex items-center space-x-1">
                      <span className="text-xs text-primary-text-secondary">Premium</span>
                      <Shield className="w-3 h-3 text-accent" />
                    </div>
                  </div>
                  <ChevronDown className="w-4 h-4 text-primary-text-secondary" />
                </button>

                {/* Dropdown Menu */}
                {isMenuOpen && (
                  <div className="absolute right-0 mt-2 w-64 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg shadow-2xl shadow-card animate-fade-in">
                    <div className="p-2">
                      <a href="#profil" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                        <User className="w-4 h-4" />
                        <span className="text-primary-text-primary">Mon Profil</span>
                      </a>
                      <a href="#parametres" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                        <Settings className="w-4 h-4" />
                        <span className="text-primary-text-primary">Parametres</span>
                      </a>
                      <hr className="border-primary-border/DEFAULT my-2" />
                      <a href="#logout" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                        <LogOut className="w-4 h-4" />
                        <span className="text-primary-text-primary">Deconnexion</span>
                      </a>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-primary-bg/95 backdrop-blur-lg z-40 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        >
          <div className="bg-primary-elevated h-full w-64 shadow-2xl animate-slide-up" onClick={(e) => e.stopPropagation()}>
            <div className="p-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-primary-text-primary">Menu</h2>
                <button onClick={() => setIsSidebarOpen(false)}>
                  <X className="w-5 h-5 text-primary-text-secondary" />
                </button>
              </div>
              <nav className="space-y-2">
                <a href="#accueil" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <Home className="w-4 h-4" />
                  <span className="text-primary-text-primary">Accueil</span>
                </a>
                <a href="#marche" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <TrendingUp className="w-4 h-4" />
                  <span className="text-primary-text-primary">Marche</span>
                </a>
                <a href="#estimation" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <Target className="w-4 h-4" />
                  <span className="text-primary-text-primary">Estimation</span>
                </a>
                <a href="#dashboard" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <BarChart3 className="w-4 h-4" />
                  <span className="text-primary-text-primary">Dashboard</span>
                </a>
              </nav>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
