import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { 
  Search, Filter, Heart, Eye, MapPin, Calendar, Fuel, 
  Grid, List, SlidersHorizontal, X, Check, Star, 
  TrendingUp, Car, ChevronLeft, ChevronRight,
  Gauge, Zap, Info, ArrowUpDown, Trash2
} from 'lucide-react';
import { debounce } from 'lodash';

// --- Sub-components ---

const Badge = ({ children, color = 'accent' }) => {
  const colors = {
    accent: 'bg-accent/10 text-accent border-accent/20',
    success: 'bg-success/10 text-success border-success/20',
    warning: 'bg-warning/10 text-warning border-warning/20',
    danger: 'bg-danger/10 text-danger border-danger/20',
    secondary: 'bg-primary-elevated text-primary-text-secondary border-primary-border/DEFAULT'
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${colors[color]}`}>
      {children}
    </span>
  );
};

const AnnonceSkeleton = () => (
  <div className="bg-primary-card border border-primary-border/DEFAULT rounded-2xl overflow-hidden animate-pulse">
    <div className="h-48 bg-primary-elevated" />
    <div className="p-5 space-y-4">
      <div className="h-6 bg-primary-elevated rounded w-3/4" />
      <div className="h-8 bg-primary-elevated rounded w-1/2" />
      <div className="grid grid-cols-2 gap-4">
        <div className="h-4 bg-primary-elevated rounded" />
        <div className="h-4 bg-primary-elevated rounded" />
      </div>
    </div>
  </div>
);

const PriceComparisonBar = ({ price, estimated }) => {
  if (!estimated) return null;
  const diff = estimated - price;
  const pct = (diff / estimated) * 100;
  const isGood = diff > 0;
  
  return (
    <div className="mt-4 pt-4 border-t border-primary-border/DEFAULT">
      <div className="flex justify-between items-center mb-2">
        <span className="text-[11px] text-primary-text-secondary uppercase font-bold tracking-tight">Analyse de prix</span>
        <span className={`text-xs font-bold ${isGood ? 'text-success' : 'text-danger'}`}>
          {isGood ? `-${Math.abs(pct).toFixed(1)}% sous le marché` : `+${Math.abs(pct).toFixed(1)}% au dessus`}
        </span>
      </div>
      <div className="h-1.5 bg-primary-elevated rounded-full overflow-hidden flex">
        <div 
          className={`h-full transition-all duration-500 ${isGood ? 'bg-success' : 'bg-danger'}`}
          style={{ width: `${Math.min(Math.max(50 + (pct * 2), 5), 95)}%` }}
        />
      </div>
      <div className="flex justify-between mt-1 text-[10px] text-primary-text-secondary">
        <span>Prix Bas</span>
        <span>Moyenne: {Math.round(estimated).toLocaleString()}€</span>
        <span>Prix Haut</span>
      </div>
    </div>
  );
};

// --- Main Component ---

export default function Annonces() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { isAuthenticated } = useSelector((state) => state.user);
  
  // State
  const [annonces, setAnnonces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [favorites, setFavorites] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [showMobileFilters, setShowMobileFilters] = useState(false);

  // Derived Filters from URL
  const filters = useMemo(() => ({
    search: searchParams.get('search') || '',
    marque: searchParams.get('marque') || '',
    prix_min: searchParams.get('prix_min') || '',
    prix_max: searchParams.get('prix_max') || '',
    km_max: searchParams.get('km_max') || '',
    annee_min: searchParams.get('annee_min') || '',
    carburant: searchParams.get('carburant') || '',
    boite: searchParams.get('boite') || '',
    pays: searchParams.get('pays') || '',
    bonne_affaire: searchParams.get('bonne_affaire') === 'true',
    sort: searchParams.get('sort') || '-date_publication',
    page: parseInt(searchParams.get('page') || '1')
  }), [searchParams]);

  // Fetch Logic
  const fetchAnnonces = useCallback(async () => {
    setLoading(true);
    const query = new URLSearchParams();
    if (filters.search) query.append('search', filters.search);
    if (filters.marque) query.append('vehicule__marque', filters.marque);
    if (filters.prix_min) query.append('prix__gte', filters.prix_min);
    if (filters.prix_max) query.append('prix__lte', filters.prix_max);
    if (filters.km_max) query.append('kilometrage__lte', filters.km_max);
    if (filters.annee_min) query.append('annee__gte', filters.annee_min);
    if (filters.carburant) query.append('carburant', filters.carburant);
    if (filters.boite) query.append('boite', filters.boite);
    if (filters.pays) query.append('pays', filters.pays);
    if (filters.bonne_affaire) query.append('est_bonne_affaire', 'true');
    query.append('ordering', filters.sort);
    query.append('page', filters.page.toString());

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/annonces/?${query.toString()}`);
      const data = await response.json();
      setAnnonces(data.results || []);
      setTotalCount(data.count || 0);
    } catch (err) {
      console.error("Failed to fetch annonces", err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchAnnonces();
  }, [fetchAnnonces]);

  // Handlers
  const updateFilter = (updates) => {
    const newParams = new URLSearchParams(searchParams);
    Object.entries(updates).forEach(([key, value]) => {
      if (value === '' || value === null || value === false) {
        newParams.delete(key);
      } else {
        newParams.set(key, value);
      }
    });
    newParams.set('page', '1'); // Reset pagination on filter change
    setSearchParams(newParams);
  };

  const toggleFavorite = async (id) => {
    if (!isAuthenticated) return; // Add login modal logic?
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/annonces/${id}/toggle_favori/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (response.ok) {
        setAnnonces(prev => prev.map(a => a.id === id ? { ...a, is_favorite: !a.is_favorite } : a));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const debouncedSearch = useMemo(() => debounce((val) => updateFilter({ search: val }), 500), []);

  const activeFiltersCount = Object.keys(filters).filter(k => 
    !['sort', 'page', 'search'].includes(k) && filters[k] !== '' && filters[k] !== false
  ).length;

  return (
    <div className="min-h-screen bg-[#0D0D14] pt-24 pb-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="flex flex-col lg:flex-row gap-8">
          
          {/* Sidebar Filters */}
          <aside className={`
            lg:w-80 flex-shrink-0 space-y-6 
            ${showMobileFilters ? 'fixed inset-0 z-[60] bg-[#0D0D14] p-6 overflow-y-auto' : 'hidden lg:block'}
          `}>
            <div className="flex items-center justify-between lg:hidden mb-6">
              <h2 className="text-xl font-bold text-white">Filtres</h2>
              <button onClick={() => setShowMobileFilters(false)}><X /></button>
            </div>

            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6 space-y-8 sticky top-28">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <SlidersHorizontal size={18} className="text-accent" />
                  <span className="font-bold text-sm tracking-tight uppercase">Filtres Raffinés</span>
                </div>
                {activeFiltersCount > 0 && (
                  <button 
                    onClick={() => setSearchParams({})} 
                    className="text-[10px] uppercase font-bold text-danger hover:underline"
                  >
                    Effacer ({activeFiltersCount})
                  </button>
                )}
              </div>

              {/* Marque */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-primary-text-secondary uppercase">Marque</label>
                <div className="relative">
                  <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-primary-text-secondary" />
                  <select 
                    value={filters.marque}
                    onChange={(e) => updateFilter({ marque: e.target.value })}
                    className="w-full pl-9 pr-4 py-3 bg-primary-elevated border border-primary-border/DEFAULT rounded-xl text-sm outline-none focus:border-accent transition-all appearance-none"
                  >
                    <option value="">Toutes les marques</option>
                    <option value="Peugeot">Peugeot</option>
                    <option value="Renault">Renault</option>
                    <option value="BMW">BMW</option>
                    <option value="Mercedes">Mercedes</option>
                    <option value="Audi">Audi</option>
                    <option value="Volkswagen">Volkswagen</option>
                    <option value="Toyota">Toyota</option>
                    <option value="Ford">Ford</option>
                  </select>
                </div>
              </div>

              {/* Prix Range */}
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <label className="text-xs font-bold text-primary-text-secondary uppercase">Budget Max</label>
                  <span className="text-sm font-bold text-accent">{filters.prix_max ? `${parseInt(filters.prix_max).toLocaleString()}€` : 'Illimité'}</span>
                </div>
                <input 
                  type="range" 
                  min="0" 
                  max="100000" 
                  step="500"
                  value={filters.prix_max || 100000}
                  onChange={(e) => updateFilter({ prix_max: e.target.value === '100000' ? '' : e.target.value })}
                  className="w-full accent-accent h-1.5 bg-primary-elevated rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex gap-3">
                  <input 
                    type="number" 
                    placeholder="Min"
                    value={filters.prix_min}
                    onChange={(e) => updateFilter({ prix_min: e.target.value })}
                    className="w-1/2 bg-primary-elevated border border-primary-border/DEFAULT rounded-xl px-3 py-2 text-xs outline-none focus:border-accent"
                  />
                  <input 
                    type="number" 
                    placeholder="Max"
                    value={filters.prix_max}
                    onChange={(e) => updateFilter({ prix_max: e.target.value })}
                    className="w-1/2 bg-primary-elevated border border-primary-border/DEFAULT rounded-xl px-3 py-2 text-xs outline-none focus:border-accent"
                  />
                </div>
              </div>

              {/* Carburant - Pills */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-primary-text-secondary uppercase">Carburant</label>
                <div className="grid grid-cols-2 gap-2">
                  {['essence', 'diesel', 'electrique', 'hybride'].map(type => (
                    <button
                      key={type}
                      onClick={() => updateFilter({ carburant: filters.carburant === type ? '' : type })}
                      className={`
                        px-3 py-2 rounded-xl text-[11px] font-bold capitalize transition-all border
                        ${filters.carburant === type 
                          ? 'bg-accent border-accent text-white shadow-lg shadow-accent/20' 
                          : 'bg-primary-elevated border-primary-border/DEFAULT text-primary-text-secondary hover:border-primary-text-secondary'}
                      `}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Boite - Toggle */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-primary-text-secondary uppercase">Transmission</label>
                <div className="flex bg-primary-elevated p-1 rounded-2xl border border-primary-border/DEFAULT">
                   <button 
                     onClick={() => updateFilter({ boite: 'manuelle' })}
                     className={`flex-1 py-2 text-[11px] font-bold rounded-xl transition-all ${filters.boite === 'manuelle' ? 'bg-primary-card text-white shadow-sm' : 'text-primary-text-secondary'}`}
                   >
                     Manuelle
                   </button>
                   <button 
                     onClick={() => updateFilter({ boite: 'automatique' })}
                     className={`flex-1 py-2 text-[11px] font-bold rounded-xl transition-all ${filters.boite === 'automatique' ? 'bg-primary-card text-white shadow-sm' : 'text-primary-text-secondary'}`}
                   >
                     Automatique
                   </button>
                </div>
              </div>

              {/* Toggle Bonnes Affaires */}
              <button 
                onClick={() => updateFilter({ bonne_affaire: !filters.bonne_affaire })}
                className={`
                  w-full flex items-center justify-between p-4 rounded-2xl border transition-all
                  ${filters.bonne_affaire 
                    ? 'bg-success/5 border-success text-success shadow-lg shadow-success/10' 
                    : 'bg-primary-elevated border-primary-border/DEFAULT text-primary-text-secondary'}
                `}
              >
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${filters.bonne_affaire ? 'bg-success text-white' : 'bg-primary-card'}`}>
                    <TrendingUp size={16} />
                  </div>
                  <span className="text-sm font-bold">Pépites Uniquement</span>
                </div>
                <div className={`w-8 h-4 rounded-full relative transition-colors ${filters.bonne_affaire ? 'bg-success' : 'bg-primary-border/20'}`}>
                  <div className={`absolute top-1 w-2 h-2 bg-white rounded-full transition-all ${filters.bonne_affaire ? 'right-1' : 'left-1'}`} />
                </div>
              </button>
              
              <button 
               onClick={() => setShowMobileFilters(false)}
               className="lg:hidden w-full bg-accent text-white py-4 rounded-2xl font-bold"
              >
                Appliquer les filtres
              </button>
            </div>
          </aside>

          {/* Results Area */}
          <main className="flex-1 space-y-6">
            
            {/* Top Bar */}
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <button 
                  onClick={() => setShowMobileFilters(true)}
                  className="lg:hidden p-3 bg-primary-elevated rounded-xl text-primary-text-secondary border border-primary-border/DEFAULT"
                >
                  <Filter size={20} />
                </button>
                <h1 className="text-xl font-black text-white">
                  {loading ? 'Recherche...' : `${totalCount} véhicule${totalCount > 1 ? 's' : ''} trouvé${totalCount > 1 ? 's' : ''}`}
                </h1>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center bg-primary-elevated rounded-xl p-1 border border-primary-border/DEFAULT">
                  <button 
                    onClick={() => setViewMode('grid')}
                    className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-primary-card text-accent shadow-sm' : 'text-primary-text-secondary'}`}
                  >
                    <Grid size={18} />
                  </button>
                  <button 
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded-lg transition-all ${viewMode === 'list' ? 'bg-primary-card text-accent shadow-sm' : 'text-primary-text-secondary'}`}
                  >
                    <List size={18} />
                  </button>
                </div>
                
                <select 
                  value={filters.sort}
                  onChange={(e) => updateFilter({ sort: e.target.value })}
                  className="bg-primary-elevated border border-primary-border/DEFAULT rounded-xl px-4 py-2.5 text-sm font-bold outline-none focus:border-accent appearance-none pr-10 relative"
                  style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'24\' height=\'24\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%23888\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Cpath d=\'m6 9 6 6 6-6\'/%3E%3C/svg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 10px center', backgroundSize: '16px' }}
                >
                  <option value="-date_publication">Plus récentes</option>
                  <option value="prix">Prix croissant</option>
                  <option value="-prix">Prix décroissant</option>
                  <option value="kilometrage">Moins de km</option>
                  <option value="-ecart_prix">Meilleures affaires</option>
                </select>
              </div>
            </div>

            {/* Tags area */}
            {activeFiltersCount > 0 && (
              <div className="flex flex-wrap gap-2 animate-fade-in">
                {Object.entries(filters).map(([key, value]) => {
                  if (['sort', 'page', 'search'].includes(key) || !value || value === false) return null;
                  return (
                    <button 
                      key={key}
                      onClick={() => updateFilter({ [key]: '' })}
                      className="group flex items-center gap-2 bg-accent/5 border border-accent/20 px-3 py-1.5 rounded-full text-[11px] font-bold text-accent hover:bg-accent/10 transition-all"
                    >
                      <span>{key.replace('_', ' ')}: {value.toString()}</span>
                      <X size={12} className="opacity-50 group-hover:opacity-100" />
                    </button>
                  );
                })}
              </div>
            )}

            {/* List/Grid Container */}
            <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3' : 'grid-cols-1'}`}>
              {loading ? (
                Array(6).fill(0).map((_, i) => <AnnonceSkeleton key={i} />)
              ) : annonces.length > 0 ? (
                annonces.map((annonce) => (
                  <div 
                    key={annonce.id} 
                    className={`
                      group bg-primary-card border border-primary-border/DEFAULT rounded-[2rem] overflow-hidden 
                      hover:border-accent/40 transition-all duration-500 shadow-xl shadow-transparent hover:shadow-accent/5
                      ${viewMode === 'list' ? 'flex flex-col md:flex-row' : 'flex flex-col'}
                    `}
                  >
                    {/* Image Area */}
                    <div className={`relative bg-primary-elevated overflow-hidden ${viewMode === 'list' ? 'md:w-72 h-64 md:h-auto' : 'h-60'}`}>
                      <div className="absolute inset-0 flex items-center justify-center text-4xl opacity-20 grayscale group-hover:grayscale-0 group-hover:scale-110 transition-all duration-700">
                        🚗
                      </div>
                      <div className="absolute top-4 left-4 flex flex-col gap-2 z-10">
                        {annonce.est_bonne_affaire && <Badge color="success">Pépite</Badge>}
                        {annonce.pays && <Badge color="secondary">{annonce.pays}</Badge>}
                      </div>
                      <button 
                        onClick={(e) => { e.preventDefault(); toggleFavorite(annonce.id); }}
                        className={`
                          absolute top-4 right-4 p-2.5 rounded-xl border transition-all z-10
                          ${annonce.is_favorite 
                            ? 'bg-accent border-accent text-white shadow-lg shadow-accent/40' 
                            : 'bg-black/20 backdrop-blur-md border-white/10 text-white hover:bg-accent hover:border-accent'}
                        `}
                      >
                        <Heart size={16} className={annonce.is_favorite ? 'fill-white' : ''} />
                      </button>
                      <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end z-10 opacity-0 transform translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300">
                         <div className="bg-black/40 backdrop-blur-md px-3 py-1 rounded-lg text-[10px] font-bold text-white uppercase">
                            {annonce.ville || 'Région Inconnue'}
                         </div>
                         <div className="flex gap-2">
                            <button className="p-2 bg-white rounded-lg text-black hover:bg-accent hover:text-white transition-colors"><Eye size={14}/></button>
                         </div>
                      </div>
                    </div>

                    {/* Content Area */}
                    <div className="p-6 flex flex-col flex-1">
                      <div className="flex justify-between items-start mb-1">
                        <span className="text-[10px] font-extrabold text-accent uppercase tracking-[0.2em]">
                          {annonce.vehicule_marque}
                        </span>
                        <div className="flex items-center gap-1 text-primary-text-secondary">
                           <Star size={10} className="fill-warning text-warning" />
                           <span className="text-[10px] font-bold">4.8</span>
                        </div>
                      </div>
                      <h3 className="text-lg font-bold text-white mb-4 line-clamp-1 group-hover:text-accent transition-colors">
                        {annonce.vehicule_modele} {annonce.annee}
                      </h3>

                      <div className="grid grid-cols-2 gap-4 mb-6">
                        <div className="flex items-center gap-2 text-primary-text-secondary">
                          <Gauge size={14} />
                          <span className="text-xs font-medium">{annonce.kilometrage?.toLocaleString()} km</span>
                        </div>
                        <div className="flex items-center gap-2 text-primary-text-secondary">
                          <Zap size={14} />
                          <span className="text-xs font-medium uppercase">{annonce.carburant}</span>
                        </div>
                      </div>

                      <div className="mt-auto">
                        <div className="flex items-end justify-between">
                          <div className="flex flex-col">
                            <span className="text-xs text-primary-text-secondary font-medium">Prix Final</span>
                            <span className="text-2xl font-black text-white">{annonce.prix?.toLocaleString()}€</span>
                          </div>
                          <button className="bg-primary-elevated hover:bg-accent text-white px-5 py-2.5 rounded-2xl text-sm font-bold transition-all border border-primary-border/DEFAULT hover:border-accent group/btn">
                             Détails 
                             <ArrowUpDown size={14} className="inline ml-2 group-hover/btn:rotate-180 transition-transform" />
                          </button>
                        </div>
                        
                        {/* Comparison logic integrated */}
                        <PriceComparisonBar price={annonce.prix} estimated={annonce.prix_estime} />
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-span-full py-20 text-center space-y-6 animate-fade-in">
                   <div className="w-20 h-20 bg-primary-card rounded-[2.5rem] flex items-center justify-center mx-auto border border-primary-border/DEFAULT">
                      <Trash2 size={32} className="text-primary-text-secondary" />
                   </div>
                   <div className="space-y-2">
                     <h3 className="text-2xl font-bold text-white">Oops, c'est le désert !</h3>
                     <p className="text-primary-text-secondary max-w-sm mx-auto">
                       Aucun véhicule ne correspond à vos critères d'élite. Essayez d'être un peu moins exigeant (juste un peu).
                     </p>
                   </div>
                   <button 
                    onClick={() => setSearchParams({})}
                    className="bg-accent text-white px-8 py-4 rounded-2xl font-bold hover:scale-105 transition-transform"
                   >
                     Réinitialiser tout
                   </button>
                </div>
              )}
            </div>

            {/* Pagination */}
            {totalCount > 0 && (
              <div className="flex justify-center items-center gap-4 pt-10">
                <button 
                  disabled={filters.page === 1}
                  onClick={() => updateFilter({ page: filters.page - 1 })}
                  className="p-3 bg-primary-card border border-primary-border/DEFAULT rounded-2xl text-white disabled:opacity-30 disabled:cursor-not-allowed hover:border-accent transition-all"
                >
                  <ChevronLeft size={20} />
                </button>
                <div className="flex gap-2">
                  <span className="px-5 py-3 bg-accent text-white rounded-2xl font-black shadow-lg shadow-accent/20">
                    {filters.page}
                  </span>
                </div>
                <button 
                  disabled={filters.page * 10 >= totalCount}
                  onClick={() => updateFilter({ page: filters.page + 1 })}
                  className="p-3 bg-primary-card border border-primary-border/DEFAULT rounded-2xl text-white disabled:opacity-30 disabled:cursor-not-allowed hover:border-accent transition-all"
                >
                  <ChevronRight size={20} />
                </button>
              </div>
            )}

          </main>
        </div>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
      `}</style>
    </div>
  );
}
