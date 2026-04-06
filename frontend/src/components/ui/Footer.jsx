import React from 'react'
import { Link } from 'react-router-dom'
import { Car, Mail, Phone, Github, Twitter, Linkedin } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-primary-bg border-t border-primary-border/DEFAULT py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="col-span-2 md:col-span-1">
            <Link to="/" className="flex items-center space-x-2 mb-4 group">
              <Car className="w-6 h-6 text-accent group-hover:scale-110 transition-transform" />
              <h3 className="text-xl font-bold text-white">AutoIntel</h3>
            </Link>
            <p className="text-primary-text-secondary text-sm leading-relaxed">
              L'intelligence artificielle au service de l'automobile. Estimez, analysez et trouvez les meilleures opportunités du marché.
            </p>
            <div className="flex items-center space-x-4 mt-6">
              <a href="#" className="p-2 bg-primary-card rounded-lg text-primary-text-secondary hover:text-white transition-colors">
                <Twitter className="w-4 h-4" />
              </a>
              <a href="#" className="p-2 bg-primary-card rounded-lg text-primary-text-secondary hover:text-white transition-colors">
                <Github className="w-4 h-4" />
              </a>
              <a href="#" className="p-2 bg-primary-card rounded-lg text-primary-text-secondary hover:text-white transition-colors">
                <Linkedin className="w-4 h-4" />
              </a>
            </div>
          </div>
          
          <div>
            <h4 className="font-bold text-white mb-6 uppercase tracking-wider text-xs">Produit</h4>
            <ul className="space-y-3">
              <li><Link to="/estimation" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Estimation</Link></li>
              <li><Link to="/annonces" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Marché</Link></li>
              <li><Link to="/dashboard" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Tableau de bord</Link></li>
              <li><Link to="/alertes" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Alertes Prix</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-bold text-white mb-6 uppercase tracking-wider text-xs">Ressources</h4>
            <ul className="space-y-3">
              <li><Link to="/statistiques" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Analyses</Link></li>
              <li><Link to="/marques" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Marques</Link></li>
              <li><Link to="/modeles" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Modèles</Link></li>
              <li><a href="#" className="text-primary-text-secondary hover:text-accent transition-colors text-sm">Documentation API</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-bold text-white mb-6 uppercase tracking-wider text-xs">Contact</h4>
            <ul className="space-y-4">
              <li className="flex items-start space-x-3">
                <Mail className="w-4 h-4 text-accent mt-0.5" />
                <span className="text-primary-text-secondary text-sm">contact@autointel.dz</span>
              </li>
              <li className="flex items-start space-x-3">
                <Phone className="w-4 h-4 text-accent mt-0.5" />
                <span className="text-primary-text-secondary text-sm">+213 (0) 555 12 34 56</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-primary-border/DEFAULT mt-12 pt-8 flex flex-col md:flex-row justify-between items-center group">
          <p className="text-primary-text-secondary text-sm">&copy; 2024 AutoIntel. Tous droits réservés.</p>
          <div className="flex space-x-6 mt-4 md:mt-0 text-sm">
            <a href="#" className="text-primary-text-secondary hover:text-white transition-colors">Confidentialité</a>
            <a href="#" className="text-primary-text-secondary hover:text-white transition-colors">CGU</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
