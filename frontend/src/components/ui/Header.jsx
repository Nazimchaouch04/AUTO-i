import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { logoutUser } from '../../store/userSlice'
import { Bell, Search, Menu, X, TrendingUp, Users, Car, Settings, LogOut, Home, BarChart3, PieChart, Tag, Target, ChevronDown, User, Shield, Star, ArrowRight, Crown, Coins, ShoppingCart } from 'lucide-react'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [notifications, setNotifications] = useState(3)
  
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { user, profil, isAuthenticated } = useSelector((state) => state.user)

  const handleLogout = () => {
    dispatch(logoutUser())
    setIsMenuOpen(false)
    navigate('/')
  }

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
              
              <Link to="/" className="flex items-center space-x-3 group">
                <div className="relative">
                  <div className="absolute inset-0 bg-accent rounded-lg p-1 group-hover:scale-110 transition-transform">
                    <Car className="w-5 h-5 text-white" />
                  </div>
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-success rounded-full flex items-center justify-center">
                    <span className="text-white text-xs font-bold">AI</span>
                  </div>
                </div>
                <h1 className="text-xl font-bold text-primary-text-primary hidden sm:block">AutoIntel</h1>
              </Link>
            </div>

            {/* Navigation Desktop */}
            <nav className="hidden lg:flex items-center space-x-6">
              <Link to="/" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <Home className="w-4 h-4" />
                <span>Accueil</span>
              </Link>
              <Link to="/annonces" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>Marche</span>
              </Link>
              <Link to="/estimation" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <Target className="w-4 h-4" />
                <span>Estimation</span>
              </Link>
              <Link to="/dashboard" className="text-primary-text-secondary hover:text-white transition-colors duration-200 flex items-center space-x-2">
                <BarChart3 className="w-4 h-4" />
                <span>Dashboard</span>
              </Link>
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
                <Link to="/alertes" className="relative p-2 text-primary-text-secondary hover:text-white transition-colors duration-200 block">
                  <Bell className="w-5 h-5" />
                  {notifications > 0 && (
                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-danger rounded-full flex items-center justify-center animate-pulse-slow">
                      <span className="text-white text-xs font-bold">{notifications}</span>
                    </span>
                  )}
                </Link>
              </div>

              {/* User Menu */}
              <div className="relative">
                {isAuthenticated ? (
                  <>
                    <button 
                      onClick={() => setIsMenuOpen(!isMenuOpen)}
                      className="flex items-center space-x-3 bg-primary-card border border-primary-border/DEFAULT rounded-lg px-4 py-2 text-primary-text-primary hover:bg-primary-elevated transition-all duration-200"
                    >
                      <div className="flex items-center gap-2 bg-yellow-500/10 border border-yellow-500/20 px-2 py-1 rounded-lg mr-2 shrink-0">
                        <Coins className="w-3 h-3 text-yellow-500" />
                        <span className="text-[10px] font-black text-yellow-500">{profil?.autocoin_balance || 0}</span>
                      </div>
                      <div className="w-8 h-8 bg-gradient-to-r from-accent to-accent-secondary rounded-full flex items-center justify-center">
                        <User className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex flex-col items-start min-w-[80px]">
                        <span className="text-sm font-medium text-primary-text-primary">{user?.username || 'Utilisateur'}</span>
                        <div className="flex items-center space-x-1">
                          <span className="text-xs text-primary-text-secondary">{profil?.nom_niveau || 'Apprenti'}</span>
                          <Shield className="w-3 h-3 text-accent" />
                        </div>
                      </div>
                      <ChevronDown className={`w-4 h-4 text-primary-text-secondary transition-transform ${isMenuOpen ? 'rotate-180' : ''}`} />
                    </button>

                    {/* Dropdown Menu */}
                    {isMenuOpen && (
                      <div className="absolute right-0 mt-2 w-64 bg-primary-elevated border border-primary-border/DEFAULT rounded-lg shadow-2xl shadow-card animate-fade-in overflow-hidden">
                        <div className="p-2">
                          <Link to="/profil" onClick={() => setIsMenuOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                            <User className="w-4 h-4 text-accent" />
                            <span className="text-primary-text-primary text-sm font-medium">Mon Profil</span>
                          </Link>
                          <Link to="/statistiques" onClick={() => setIsMenuOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                            <BarChart3 className="w-4 h-4 text-success" />
                            <span className="text-primary-text-primary text-sm font-medium">Statistiques</span>
                          </Link>
                          <Link to="/alertes" onClick={() => setIsMenuOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                            <Bell className="w-4 h-4 text-warning" />
                            <span className="text-primary-text-primary text-sm font-medium">Mes Alertes</span>
                          </Link>
                          <Link to="/shop" onClick={() => setIsMenuOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                            <ShoppingCart className="w-4 h-4 text-success" />
                            <span className="text-primary-text-primary text-sm font-medium">Boutique</span>
                          </Link>
                          <Link to="/battles" onClick={() => setIsMenuOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                            <Swords className="w-4 h-4 text-accent" />
                            <span className="text-primary-text-primary text-sm font-medium">L'Arène</span>
                          </Link>
                          <Link to="/pricing" onClick={() => setIsMenuOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-accent/10 border border-transparent hover:border-accent/20 transition-colors duration-200">
                            <Crown className="w-4 h-4 text-accent" />
                            <span className="text-accent text-sm font-bold">Passer Pro</span>
                          </Link>
                          <hr className="border-primary-border/DEFAULT my-2" />
                          <button 
                            onClick={handleLogout}
                            className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-danger/10 text-danger transition-colors duration-200"
                          >
                            <LogOut className="w-4 h-4" />
                            <span className="text-sm font-medium">Déconnexion</span>
                          </button>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="flex items-center space-x-3">
                    <Link to="/login" className="text-sm font-medium text-primary-text-secondary hover:text-white transition-colors">
                      Connexion
                    </Link>
                    <Link to="/register" className="bg-accent hover:bg-accent-secondary text-white px-4 py-2 rounded-lg text-sm font-bold transition-all shadow-lg shadow-accent/20">
                      S'inscrire
                    </Link>
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
                <Link to="/" onClick={() => setIsSidebarOpen(false)} className="text-lg font-bold text-primary-text-primary flex items-center space-x-2">
                   <Car className="w-5 h-5 text-accent" />
                   <span>AutoIntel</span>
                </Link>
                <button onClick={() => setIsSidebarOpen(false)}>
                  <X className="w-5 h-5 text-primary-text-secondary" />
                </button>
              </div>
              <nav className="space-y-2">
                <Link to="/" onClick={() => setIsSidebarOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <Home className="w-4 h-4 text-accent" />
                  <span className="text-primary-text-primary">Accueil</span>
                </Link>
                <Link to="/annonces" onClick={() => setIsSidebarOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <TrendingUp className="w-4 h-4 text-success" />
                  <span className="text-primary-text-primary">Marche</span>
                </Link>
                <Link to="/estimation" onClick={() => setIsSidebarOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <Target className="w-4 h-4 text-warning" />
                  <span className="text-primary-text-primary">Estimation</span>
                </Link>
                <Link to="/dashboard" onClick={() => setIsSidebarOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <BarChart3 className="w-4 h-4 text-accent-secondary" />
                  <span className="text-primary-text-primary">Dashboard</span>
                </Link>
                <Link to="/battles" onClick={() => setIsSidebarOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-primary-card transition-colors duration-200">
                  <Swords className="w-4 h-4 text-accent" />
                  <span className="text-primary-text-primary">L'Arène</span>
                </Link>
                <Link to="/pricing" onClick={() => setIsSidebarOpen(false)} className="flex items-center space-x-3 px-3 py-2 rounded-lg bg-accent/10 border border-accent/20 transition-colors duration-200">
                  <Crown className="w-4 h-4 text-accent" />
                  <span className="text-accent font-bold">Offres Pro</span>
                </Link>
              </nav>

              {!isAuthenticated && (
                <div className="mt-8 space-y-3 pt-8 border-t border-primary-border/DEFAULT">
                  <Link to="/login" onClick={() => setIsSidebarOpen(false)} className="flex items-center justify-center w-full px-4 py-3 rounded-xl border border-primary-border/DEFAULT text-primary-text-primary font-bold">
                    Connexion
                  </Link>
                  <Link to="/register" onClick={() => setIsSidebarOpen(false)} className="flex items-center justify-center w-full px-4 py-3 rounded-xl bg-accent text-white font-bold shadow-lg shadow-accent/20">
                    S'inscrire
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  )
}
