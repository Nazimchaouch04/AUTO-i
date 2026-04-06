import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Play } from 'lucide-react'

export default function Hero() {
  return (
    <section id="accueil" className="relative pt-32 pb-20 overflow-hidden bg-primary">
      {/* Background gradients */}
      <div className="absolute top-0 right-0 w-1/3 h-1/3 bg-accent/5 blur-[120px] -z-10" />
      <div className="absolute bottom-0 left-0 w-1/4 h-1/4 bg-accent-secondary/5 blur-[120px] -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="inline-flex items-center space-x-2 bg-primary-card border border-primary-border/DEFAULT rounded-full px-4 py-1.5 mb-8 animate-fade-in-down">
          <span className="w-2 h-2 bg-accent rounded-full animate-pulse" />
          <span className="text-xs font-bold text-primary-text-secondary uppercase tracking-widest">Nouveauté : Estimation IA v2.5</span>
        </div>

        <h2 className="text-4xl md:text-6xl lg:text-7xl font-extrabold text-white mb-8 leading-[1.1] tracking-tight animate-fade-in">
          L'intelligence artificielle au service de <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-accent-secondary">l'automobile</span>
        </h2>
        
        <p className="text-lg md:text-xl text-primary-text-secondary mb-12 max-w-3xl mx-auto leading-relaxed animate-fade-in [animation-delay:200ms]">
          Estimez le prix de votre véhicule avec une précision chirurgicale, détectez les meilleures affaires en temps réel et analysez les tendances du marché automobile mondial.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 animate-fade-in [animation-delay:400ms]">
          <Link 
            to="/register" 
            className="w-full sm:w-auto bg-accent hover:bg-accent-secondary text-white px-8 py-4 rounded-2xl font-bold text-lg transition-all flex items-center justify-center space-x-3 shadow-xl shadow-accent/20 group"
          >
            <span>Commencer gratuitement</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          
          <Link 
            to="/estimation" 
            className="w-full sm:w-auto bg-primary-card hover:bg-primary-elevated border border-primary-border/DEFAULT text-white px-8 py-4 rounded-2xl font-bold text-lg transition-all flex items-center justify-center space-x-3 group"
          >
            <Play className="w-4 h-4 fill-white group-hover:scale-110 transition-transform" />
            <span>Essayer l'estimateur</span>
          </Link>
        </div>

        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
           <div className="font-black text-2xl text-primary-text-secondary">AUTO-P</div>
           <div className="font-black text-2xl text-primary-text-secondary">INTELLI-CAR</div>
           <div className="font-black text-2xl text-primary-text-secondary">CAR-STAT</div>
           <div className="font-black text-2xl text-primary-text-secondary">MARKET-AI</div>
        </div>
      </div>
    </section>
  )
}
