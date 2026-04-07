import React, { useState, useEffect, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  User, Heart, History, Bell, CreditCard, Award, 
  Settings, LogOut, ChevronRight, Edit3, Save, 
  Trash2, ExternalLink, Zap, Shield, TrendingUp,
  Mail, Calendar, MapPin, CheckCircle2, AlertCircle,
  LayoutDashboard, ArrowRight, Search, PieChart
} from 'lucide-react';
import { fetchProfile } from '../../store/userSlice';
import { debounce } from 'lodash';
import { useNavigate } from 'react-router-dom';
import { SkeletonCard, SkeletonKPI } from '../ui/Skeleton';
import PageTransition from '../ui/PageTransition';
import ExportButton from '../ui/ExportButton';
import axiosClient from '../../api/axiosClient';

// --- Sub-components for Sections ---

const SectionHeader = ({ title, description, badge }) => (
  <div className="mb-8">
    <div className="flex items-center gap-3 mb-1">
      <h2 className="text-2xl font-black text-white tracking-tight">{title}</h2>
      {badge && (
        <span className="px-2 py-0.5 bg-accent/10 border border-accent/20 text-accent text-[10px] font-bold rounded-full uppercase tracking-wider">
          {badge}
        </span>
      )}
    </div>
    <p className="text-primary-text-secondary text-sm">{description}</p>
  </div>
);

// --- 1. Home Section (Overview) ---
const HomeSection = ({ user, stats, medailles, onNavigate }) => (
  <div className="space-y-8 animate-fade-in">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6 relative overflow-hidden group hover:border-accent transition-all cursor-pointer" onClick={() => onNavigate('favoris')}>
        <div className="absolute -right-4 -top-4 w-24 h-24 bg-accent/5 rounded-full blur-2xl group-hover:bg-accent/10 transition-all"></div>
        <div className="flex flex-col h-full">
          <Heart className="text-accent mb-4" size={24} />
          <span className="text-4xl font-black text-white mb-1">{stats?.favoris_count || 0}</span>
          <span className="text-sm text-primary-text-secondary font-bold uppercase tracking-wider">Favoris</span>
        </div>
      </div>
      <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6 relative overflow-hidden group hover:border-accent transition-all cursor-pointer" onClick={() => onNavigate('recherches')}>
        <div className="absolute -right-4 -top-4 w-24 h-24 bg-warning/5 rounded-full blur-2xl group-hover:bg-warning/10 transition-all"></div>
        <div className="flex flex-col h-full">
          <History className="text-warning mb-4" size={24} />
          <span className="text-4xl font-black text-white mb-1">{stats?.recherches_count || 0}</span>
          <span className="text-sm text-primary-text-secondary font-bold uppercase tracking-wider">Recherches</span>
        </div>
      </div>
      <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6 relative overflow-hidden group hover:border-accent transition-all cursor-pointer" onClick={() => onNavigate('medailles')}>
         <div className="absolute -right-4 -top-4 w-24 h-24 bg-success/5 rounded-full blur-2xl group-hover:bg-success/10 transition-all"></div>
         <div className="flex flex-col h-full">
          <Award className="text-success mb-4" size={24} />
          <span className="text-4xl font-black text-white mb-1">{medailles?.length || 0}</span>
          <span className="text-sm text-primary-text-secondary font-bold uppercase tracking-wider">Médailles</span>
        </div>
      </div>
    </div>

    <div className="bg-accent/5 border border-accent/20 rounded-[2.5rem] p-8 flex flex-col md:flex-row items-center gap-8 shadow-xl shadow-accent/5">
      <div className="relative">
        <div className="w-24 h-24 bg-accent rounded-full flex items-center justify-center text-3xl font-black text-white shadow-2xl shadow-accent/40 ring-4 ring-white/10">
          {user?.username?.charAt(0).toUpperCase()}
        </div>
        <div className="absolute -bottom-1 -right-1 w-8 h-8 bg-success border-4 border-[#0D0D14] rounded-full flex items-center justify-center">
           <Zap size={14} className="text-white" />
        </div>
      </div>
      <div className="flex-1 text-center md:text-left">
        <h3 className="text-2xl font-black text-white mb-1">Bienvenue, {user?.username} !</h3>
        <p className="text-primary-text-secondary mb-4">Votre niveau d'expertise automobile : <span className="text-accent font-bold">Apprenti Mécanicien</span></p>
        <div className="w-full max-w-md h-2 bg-primary-elevated rounded-full overflow-hidden">
           <div className="h-full bg-accent w-1/3 shadow-lg shadow-accent/40"></div>
        </div>
        <div className="mt-2 text-[10px] text-primary-text-secondary font-bold uppercase tracking-widest flex justify-between max-w-md">
           <span>Niv. 1</span>
           <span>Niv. 2 : 500 XP pour passer</span>
        </div>
      </div>
      <button className="bg-white text-black px-8 py-3 rounded-2xl font-bold hover:scale-105 transition-transform" onClick={() => onNavigate('abonnement')}>
         Passer Pro
      </button>
    </div>

    <div className="bg-primary-card border border-primary-border/DEFAULT rounded-[2.5rem] p-8">
       <div className="flex items-center gap-3 mb-6">
         <TrendingUp className="text-success" size={20} />
         <h3 className="text-lg font-black text-white">Activité du Compte</h3>
         <div className="ml-auto">
            <ExportButton 
              endpoint="/api/estimation/export_mes_estimations/" 
              filename="mes_estimations.csv" 
              label="Télécharger mes données" 
            />
         </div>
       </div>
       <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
         <div className="space-y-4">
           <p className="text-xs text-primary-text-secondary font-bold uppercase tracking-widest">Performances</p>
           <div className="flex justify-between items-center bg-primary-elevated p-4 rounded-2xl">
             <span className="text-primary-text-secondary font-medium">Recherches effectuées</span>
             <span className="text-white font-black">{stats?.recherches_count || 0}</span>
           </div>
           <div className="flex justify-between items-center bg-primary-elevated p-4 rounded-2xl">
             <span className="text-primary-text-secondary font-medium">Alertes actives</span>
             <span className="text-white font-black">{stats?.alertes_count || 0}</span>
           </div>
         </div>
         <div className="flex flex-col justify-center items-center p-6 bg-accent/5 border border-accent/20 rounded-3xl">
           <PieChart size={40} className="text-accent mb-4" />
           <p className="text-sm font-bold text-white mb-1">Analyse des préférences</p>
           <p className="text-[10px] text-primary-text-secondary text-center">Basé sur vos {stats?.favoris_count || 0} favoris et recherches.</p>
         </div>
       </div>
    </div>
  </div>
);

// --- 2. Profile Section ---
const ProfileSection = ({ user, onUpdate }) => {
  const [formData, setFormData] = useState({ username: user?.username || '', email: user?.email || '' });
  const [isSaving, setIsSaving] = useState(false);

  const debouncedUpdate = useMemo(() => debounce(async (data) => {
    setIsSaving(true);
    await onUpdate(data);
    setIsSaving(false);
  }, 1000), [onUpdate]);

  const handleChange = (e) => {
    const newData = { ...formData, [e.target.name]: e.target.value };
    setFormData(newData);
    debouncedUpdate(newData);
  };

  return (
    <div className="animate-fade-in max-w-2xl">
      <SectionHeader title="Informations Personnelles" description="Gérez votre identité AutoIntel" badge="Sécurisé" />
      <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-8 space-y-6">
        <div className="space-y-2">
          <label className="text-[10px] font-bold text-primary-text-secondary uppercase tracking-[0.2em]">Nom d'utilisateur</label>
          <div className="relative group">
            <User size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-primary-text-secondary" />
            <input 
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl pl-12 pr-4 py-4 text-white outline-none focus:border-accent transition-all"
            />
          </div>
        </div>
        <div className="space-y-2">
          <label className="text-[10px] font-bold text-primary-text-secondary uppercase tracking-[0.2em]">Email Professionnel</label>
          <div className="relative">
            <Mail size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-primary-text-secondary" />
            <input 
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl pl-12 pr-4 py-4 text-white outline-none focus:border-accent transition-all"
            />
          </div>
        </div>
        <div className="flex items-center gap-2 pt-4">
           {isSaving ? (
              <div className="flex items-center gap-2 text-accent text-xs font-bold animate-pulse">
                <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce"></div>
                Sauvegarde automatique...
              </div>
           ) : (
             <div className="flex items-center gap-2 text-success text-xs font-bold">
               <CheckCircle2 size={14} />
               Données enregistrées
             </div>
           )}
        </div>
      </div>
    </div>
  );
};

// --- 3. Favorites Section ---
const FavoritesSection = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFavs = async () => {
      try {
        const response = await axiosClient.get('/api/annonces/mes_favoris/');
        const data = response.data;
        setFavorites(data.results || []);
      } catch (e) { console.log(e); } finally { setLoading(false); }
    };
    fetchFavs();
  }, []);

  const removeFavorite = async (id) => {
     try {
       await axiosClient.post(`/api/annonces/${id}/toggle_favori/`);
       setFavorites(f => f.filter(x => x.id !== id));
     } catch(e) {}
  };

  return (
    <div className="animate-fade-in">
      <SectionHeader title="Mes Favoris" description="Votre sélection d'élite" badge={`${favorites.length} Items`} />
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {loading ? (
          Array(3).fill(0).map((_, i) => <SkeletonCard key={i} />)
        ) : favorites.length > 0 ? (
          favorites.map(f => (
            <div key={f.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl overflow-hidden group hover:border-accent transition-all">
              <div className="h-40 bg-primary-elevated flex items-center justify-center text-4xl opacity-20 grayscale group-hover:grayscale-0 transition-all">🚗</div>
              <div className="p-5">
                <h4 className="text-white font-bold mb-1">{f.vehicule_marque} {f.vehicule_modele}</h4>
                <div className="flex justify-between items-end">
                   <div className="text-sm text-primary-text-secondary">{f.annee} • {f.prix.toLocaleString()}€</div>
                   <button onClick={() => removeFavorite(f.id)} className="p-2 text-danger hover:bg-danger/10 rounded-xl transition-all">
                     <Trash2 size={16} />
                   </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full py-20 text-center bg-primary-card rounded-3xl border border-dashed border-primary-border/DEFAULT">
             <Heart size={32} className="mx-auto text-primary-text-secondary opacity-30 mb-4" />
             <p className="text-primary-text-secondary font-bold">Aucun favori pour le moment.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// --- 4. Subscription Section ---
const SubscriptionSection = ({ profile, onNavigatePricing }) => {
  const plan = profile?.abonnement?.plan_details || profile?.plan_details;
  
  return (
    <div className="animate-fade-in max-w-2xl">
      <SectionHeader title="Votre Abonnement" description="Gérez votre puissance AutoIntel" badge={plan?.nom} />
      
      <div className="bg-primary-card border border-primary-border/DEFAULT rounded-[2.5rem] p-10 relative overflow-hidden group">
        <div className="absolute -right-20 -top-20 w-64 h-64 bg-accent/5 rounded-full blur-3xl group-hover:bg-accent/10 transition-all duration-700"></div>
        
        <div className="relative z-10">
          <div className="flex items-center gap-4 mb-8">
            <div className="p-4 bg-accent/10 rounded-2xl text-accent border border-accent/20 shadow-lg shadow-accent/5">
               <Zap size={32} />
            </div>
            <div>
              <p className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest mb-1">Plan Actuel</p>
              <h3 className="text-3xl font-black text-white capitalize tracking-tight">{plan?.nom || 'Gratuit'}</h3>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-10">
            <div className="bg-primary-elevated p-4 rounded-2xl border border-primary-border/DEFAULT">
               <span className="block text-[10px] font-bold text-primary-text-secondary uppercase mb-1">Estimations</span>
               <span className="text-xl font-black text-white">{plan?.estimations_par_mois || 5} <span className="text-xs text-primary-text-secondary">/ mois</span></span>
            </div>
            <div className="bg-primary-elevated p-4 rounded-2xl border border-primary-border/DEFAULT">
               <span className="block text-[10px] font-bold text-primary-text-secondary uppercase mb-1">Alertes</span>
               <span className="text-xl font-black text-white">{plan?.alertes_max || 2} <span className="text-xs text-primary-text-secondary">actives</span></span>
            </div>
          </div>

          <button 
            onClick={onNavigatePricing}
            className="w-full bg-white text-black py-5 rounded-[1.5rem] font-black text-sm uppercase tracking-widest hover:scale-[1.02] transition-all flex items-center justify-center gap-3"
          >
            Passer à la vitesse supérieure
            <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

// --- 5. Recherches Section ---
const RecherchesSection = () => {
  const [recherches, setRecherches] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRecherches = async () => {
      try {
        const response = await axiosClient.get('/api/annonces/recherches/');
        const data = response.data;
        setRecherches(data.results || data);
      } catch (e) { console.error(e); } finally { setLoading(false); }
    };
    fetchRecherches();
  }, []);

  const deleteRecherche = async (id) => {
    try {
      await axiosClient.delete(`/api/annonces/recherches/${id}/`);
      setRecherches(r => r.filter(x => x.id !== id));
    } catch (e) {}
  };

  const handleLaunch = (r) => {
    const params = new URLSearchParams();
    if (r.marque) params.append('marque', r.marque);
    if (r.modele) params.append('modele', r.modele);
    if (r.prix_max) params.append('prix_max', r.prix_max);
    navigate(`/annonces?${params.toString()}`);
  };

  return (
    <div className="animate-fade-in">
      <SectionHeader title="Historique de Recherche" description="Vos filtres d'élite sauvegardés" badge={`${recherches.length} Recherches`} />
      <div className="space-y-4">
        {loading ? (
          Array(2).fill(0).map((_, i) => <SkeletonKPI key={i} />)
        ) : recherches.length > 0 ? (
          recherches.map(r => (
            <div key={r.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between group hover:border-accent transition-all gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-primary-elevated rounded-xl flex items-center justify-center text-accent">
                  <Search size={20} />
                </div>
                <div>
                  <h4 className="text-white font-bold">{r.marque || 'Toutes marques'} {r.modele || ''}</h4>
                  <p className="text-xs text-primary-text-secondary">
                    {r.prix_max ? `Budget max: ${parseInt(r.prix_max).toLocaleString()}€` : 'Aucune limite de prix'}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <button 
                  onClick={() => handleLaunch(r)}
                  className="px-6 py-2 bg-accent text-white text-xs font-bold rounded-xl hover:scale-105 transition-all flex items-center gap-2"
                >
                  Relancer <ExternalLink size={14} />
                </button>
                <button 
                  onClick={() => deleteRecherche(r.id)}
                  className="p-2 text-danger hover:bg-danger/10 rounded-xl transition-all"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="py-20 text-center bg-primary-card rounded-3xl border border-dashed border-primary-border/DEFAULT">
             <History size={32} className="mx-auto text-primary-text-secondary opacity-30 mb-4" />
             <p className="text-primary-text-secondary font-bold">Aucune recherche sauvegardée.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// --- Main Dashboard Shell ---

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('home');
  const { profile, loading } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchProfile());
  }, [dispatch]);

  const handleUpdateProfile = async (data) => {
    try {
      await axiosClient.put('/api/auth/profile/', data);
      dispatch(fetchProfile());
    } catch (err) {
      console.error(err);
    }
  };

  const navItems = [
    { id: 'home', icon: LayoutDashboard, label: 'Vue d\'ensemble' },
    { id: 'profil', icon: User, label: 'Profil & Compte' },
    { id: 'favoris', icon: Heart, label: 'Mes Favoris' },
    { id: 'recherches', icon: History, label: 'Historique' },
    { id: 'alertes', icon: Bell, label: 'Alertes Prix' },
    { id: 'abonnement', icon: CreditCard, label: 'Abonnement' },
    { id: 'medailles', icon: Award, label: 'Médailles & XP' },
  ];

  return (
    <PageTransition>
    <div className="min-h-screen bg-[#0D0D14] flex flex-col lg:flex-row">
      
      {/* Sidebar Navigation */}
      <aside className="lg:w-80 border-r border-primary-border/DEFAULT bg-[#0D0D14] pt-24 pb-8 flex flex-col">
        <div className="px-6 mb-10">
           <div className="flex items-center gap-4 p-4 bg-primary-card rounded-3xl border border-primary-border/DEFAULT">
              <div className="w-12 h-12 bg-accent rounded-2xl flex items-center justify-center text-white font-black text-xl">
                 {profile?.user?.username?.charAt(0).toUpperCase()}
              </div>
              <div className="overflow-hidden">
                 <p className="text-white font-bold truncate">{profile?.user?.username}</p>
                 <p className="text-[10px] text-primary-text-secondary uppercase font-bold tracking-widest truncate">{profile?.user?.email}</p>
              </div>
           </div>
        </div>

        <nav className="flex-1 px-4 space-y-1">
           {navItems.map(item => (
             <button
               key={item.id}
               onClick={() => item.id === 'alertes' ? navigate('/alertes') : setActiveTab(item.id)}
               className={`
                 w-full flex items-center gap-4 px-5 py-4 rounded-2xl text-sm font-bold transition-all
                 ${activeTab === item.id 
                   ? 'bg-accent/10 text-accent border border-accent/20' 
                   : 'text-primary-text-secondary hover:bg-primary-elevated hover:text-white border border-transparent'}
               `}
             >
               <item.icon size={20} className={activeTab === item.id ? 'text-accent' : 'text-primary-text-secondary'} />
               {item.label}
               {activeTab === item.id && <div className="ml-auto w-1.5 h-1.5 bg-accent rounded-full shadow-[0_0_8px_var(--accent)]"></div>}
             </button>
           ))}
        </nav>

        <div className="px-4 mt-8 pt-8 border-t border-primary-border/DEFAULT">
           <button className="w-full flex items-center gap-4 px-5 py-4 rounded-2xl text-sm font-bold text-danger hover:bg-danger/10 transition-all">
              <LogOut size={20} />
              Déconnexion
           </button>
        </div>
      </aside>

      {/* Content Area */}
      <main className="flex-1 pt-24 pb-20 px-4 md:px-10 overflow-y-auto">
         <div className="max-w-5xl mx-auto">
            {activeTab === 'home' && <HomeSection user={profile?.user} stats={profile?.stats} medailles={profile?.medailles} onNavigate={setActiveTab} />}
            {activeTab === 'profil' && <ProfileSection user={profile?.user} onUpdate={handleUpdateProfile} />}
            {activeTab === 'favoris' && <FavoritesSection />}
            {activeTab === 'recherches' && <RecherchesSection />}
            {activeTab === 'medailles' && (
               <div className="animate-fade-in space-y-8">
                  <SectionHeader title="Médailles & XP" description="Votre ascension vers le sommet" />
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    {profile?.medailles?.map(m => (
                       <div key={m.type} className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-8 text-center flex flex-col items-center group hover:border-accent transition-all">
                          <div className={`w-20 h-20 rounded-full flex items-center justify-center mb-4 transition-transform group-hover:scale-110
                             ${m.type === 'bronze' ? 'bg-[#CD7F32]/20 text-[#CD7F32]' : ''}
                             ${m.type === 'silver' ? 'bg-[#C0C0C0]/20 text-[#C0C0C0]' : ''}
                             ${m.type === 'gold' ? 'bg-[#FFD700]/20 text-[#FFD700]' : ''}
                          `}>
                             <Award size={40} />
                          </div>
                          <span className="text-white font-black uppercase tracking-widest text-xs">{m.nom}</span>
                       </div>
                    ))}
                  </div>
               </div>
            )}
            {activeTab === 'abonnement' && (
              <SubscriptionSection profile={profile} onNavigatePricing={() => navigate('/pricing')} />
            )}
         </div>
      </main>

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
      `}</style>
    </div>
    </PageTransition>
  );
}
