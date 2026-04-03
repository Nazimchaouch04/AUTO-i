import React, { useState, useEffect } from 'react';
import { 
  Bell, Plus, Trash2, Edit3, Mail, Smartphone, 
  Search, Filter, Calendar, BellOff, CheckCircle2, 
  AlertCircle, ChevronRight, X, Zap, Target
} from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000/api/alertes/';

export default function Alertes() {
  const [alertes, setAlertes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [formData, setFormData] = useState({
    titre: '',
    marque: '',
    modele: '',
    prix_min: '',
    prix_max: '',
    km_max: '',
    annee_min: '',
    carburant: '',
    boite_vitesse: '',
    pays: 'DZ',
    email_actif: true,
    push_actif: true,
    est_active: true
  });

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetchAlertes();
  }, []);

  const fetchAlertes = async () => {
    setLoading(true);
    try {
      const response = await fetch(API_BASE, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setAlertes(data.results || []);
    } catch (err) {
      setError("Impossible de charger vos alertes.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (alerte) => {
    try {
      const response = await fetch(`${API_BASE}${alerte.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ est_active: !alerte.est_active })
      });
      if (response.ok) fetchAlertes();
    } catch (err) { console.error(err); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Supprimer cette alerte ?")) return;
    try {
      await fetch(`${API_BASE}${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setAlertes(prev => prev.filter(a => a.id !== id));
      setSuccess("Alerte supprimée.");
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) { setError("Erreur lors de la suppression."); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `${API_BASE}${editingId}/` : API_BASE;

    // Nettoyage des données (conversions types)
    const payload = { ...formData };
    if (payload.prix_min === '') delete payload.prix_min;
    if (payload.prix_max === '') delete payload.prix_max;
    if (payload.km_max === '') delete payload.km_max;
    if (payload.annee_min === '') delete payload.annee_min;

    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(editingId ? "Alerte mise à jour !" : "Alerte créée avec succès !");
        setShowForm(false);
        setEditingId(null);
        resetForm();
        fetchAlertes();
        setTimeout(() => setSuccess(null), 3000);
      } else {
        setError(data.detail || "Une erreur est survenue.");
      }
    } catch (err) {
      setError("Erreur de connexion au serveur.");
    }
  };

  const resetForm = () => {
    setFormData({
      titre: '', marque: '', modele: '', prix_min: '', prix_max: '',
      km_max: '', annee_min: '', carburant: '', boite_vitesse: '',
      pays: 'DZ', email_actif: true, push_actif: true, est_active: true
    });
    setEditingId(null);
  };

  const startEdit = (alerte) => {
    setFormData({
      titre: alerte.titre,
      marque: alerte.marque || '',
      modele: alerte.modele || '',
      prix_min: alerte.prix_min || '',
      prix_max: alerte.prix_max || '',
      km_max: alerte.km_max || '',
      annee_min: alerte.annee_min || '',
      carburant: alerte.carburant || '',
      boite_vitesse: alerte.boite_vitesse || '',
      pays: alerte.pays || 'DZ',
      email_actif: alerte.email_actif,
      push_actif: alerte.push_actif,
      est_active: alerte.est_active
    });
    setEditingId(alerte.id);
    setShowForm(true);
  };

  return (
    <div className="min-h-screen bg-[#0D0D14] pt-28 pb-20 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div className="animate-slide-in">
            <h1 className="text-4xl font-black text-white tracking-tight mb-2 flex items-center gap-3">
               <Bell className="text-accent" size={36} />
               Mes Alertes <span className="text-accent">Smart</span>
            </h1>
            <p className="text-primary-text-secondary">Chassez les pépites du marché en temps réel.</p>
          </div>
          <button 
            onClick={() => { resetForm(); setShowForm(true); }}
            className="bg-accent text-white px-8 py-4 rounded-2xl font-bold flex items-center justify-center gap-3 hover:scale-105 transition-all shadow-xl shadow-accent/20"
          >
            <Plus size={20} />
            Nouvelle Alerte
          </button>
        </div>

        {/* Notifications (Success/Error) */}
        {error && (
          <div className="mb-8 p-4 bg-danger/10 border border-danger/20 rounded-2xl flex items-center gap-3 text-danger animate-bounce-subtle">
             <AlertCircle size={20} />
             <p className="font-bold text-sm">{error}</p>
             <button onClick={() => setError(null)} className="ml-auto"><X size={18} /></button>
          </div>
        )}
        {success && (
          <div className="mb-8 p-4 bg-success/10 border border-success/20 rounded-2xl flex items-center gap-3 text-success animate-fade-in">
             <CheckCircle2 size={20} />
             <p className="font-bold text-sm">{success}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          
          {/* Main List */}
          <div className="lg:col-span-8 space-y-6">
            {loading ? (
              [1, 2, 3].map(n => <div key={n} className="h-40 bg-primary-card rounded-3xl animate-pulse border border-primary-border/DEFAULT" />)
            ) : alertes.length > 0 ? (
              alertes.map(a => (
                <div key={a.id} className={`group bg-primary-card border transition-all duration-300 rounded-[2.5rem] p-6 md:p-8 relative overflow-hidden ${a.est_active ? 'border-primary-border/DEFAULT hover:border-accent/50' : 'border-dashed border-primary-border/30 grayscale opacity-60'}`}>
                  
                  {/* Glassmorphism accent */}
                  <div className={`absolute -right-10 -top-10 w-40 h-40 rounded-full blur-[80px] pointer-events-none transition-all duration-500 ${a.est_active ? 'bg-accent/10 opacity-100' : 'bg-white/5 opacity-0'}`}></div>

                  <div className="flex flex-col md:flex-row gap-6 relative z-10">
                    <div className={`w-16 h-16 rounded-3xl flex items-center justify-center transition-colors ${a.est_active ? 'bg-accent/10 text-accent' : 'bg-primary-elevated text-primary-text-secondary'}`}>
                       <Target size={32} />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-bold text-white">{a.titre}</h3>
                        {!a.est_active && <span className="px-2 py-0.5 bg-primary-elevated text-[10px] font-black text-primary-text-secondary uppercase rounded-full">Désactivée</span>}
                      </div>
                      
                      <div className="flex flex-wrap gap-3 text-xs text-primary-text-secondary font-bold uppercase tracking-wider">
                         {a.marque && <span className="bg-primary-elevated px-3 py-1 rounded-full">{a.marque}</span>}
                         {a.modele && <span className="bg-primary-elevated px-3 py-1 rounded-full">{a.modele}</span>}
                         {a.prix_max && <span className="bg-accent/5 text-accent px-3 py-1 rounded-full">Max {a.prix_max}€</span>}
                         {a.carburant && <span className="bg-primary-elevated px-3 py-1 rounded-full">{a.carburant}</span>}
                      </div>

                      <div className="mt-6 flex items-center gap-6">
                        <div className={`flex items-center gap-2 text-xs font-bold ${a.email_actif ? 'text-success' : 'text-primary-text-secondary'}`}>
                           <Mail size={14} /> Email {a.email_actif ? 'ON' : 'OFF'}
                        </div>
                        <div className={`flex items-center gap-2 text-xs font-bold ${a.push_actif ? 'text-success' : 'text-primary-text-secondary'}`}>
                           <Smartphone size={14} /> Push {a.push_actif ? 'ON' : 'OFF'}
                        </div>
                      </div>
                    </div>

                    <div className="flex md:flex-col justify-end gap-2">
                       <button 
                         onClick={() => handleToggleActive(a)}
                         className={`p-3 rounded-2xl transition-all ${a.est_active ? 'bg-primary-elevated text-white hover:bg-warning/20 hover:text-warning' : 'bg-success/10 text-success hover:bg-success/20'}`}
                         title={a.est_active ? "Désactiver" : "Activer"}
                       >
                         {a.est_active ? <Zap size={20} /> : <Zap size={20} />}
                       </button>
                       <button 
                         onClick={() => startEdit(a)}
                         className="p-3 bg-primary-elevated text-white rounded-2xl hover:bg-accent/20 hover:text-accent transition-all"
                       >
                         <Edit3 size={20} />
                       </button>
                       <button 
                         onClick={() => handleDelete(a.id)}
                         className="p-3 bg-primary-elevated text-white rounded-2xl hover:bg-danger/20 hover:text-danger transition-all"
                       >
                         <Trash2 size={20} />
                       </button>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="bg-primary-card border border-dashed border-primary-border/DEFAULT rounded-[2.5rem] py-24 text-center">
                 <div className="w-20 h-20 bg-primary-elevated rounded-full flex items-center justify-center mx-auto mb-6 text-primary-text-secondary opacity-30">
                    <BellOff size={40} />
                 </div>
                 <h3 className="text-xl font-bold text-white mb-2">Aucune alerte active</h3>
                 <p className="text-primary-text-secondary max-w-xs mx-auto">Créez votre première alerte pour ne rater aucune bonne affaire.</p>
              </div>
            )}
          </div>

          {/* Side Info / Global Stats */}
          <div className="lg:col-span-4 space-y-8">
             <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-8 sticky top-28">
                <h3 className="text-lg font-black text-white mb-6 flex items-center gap-2">
                   <Zap className="text-warning" size={20} />
                   Statistiques Veille
                </h3>
                <div className="space-y-4">
                   <div className="flex justify-between items-center p-4 bg-primary-elevated rounded-2xl border border-primary-border/DEFAULT">
                      <span className="text-sm text-primary-text-secondary font-bold uppercase">Alertes Actives</span>
                      <span className="text-xl font-black text-white">{alertes.filter(x => x.est_active).length}</span>
                   </div>
                   <div className="flex justify-between items-center p-4 bg-primary-elevated rounded-2xl border border-primary-border/DEFAULT">
                      <span className="text-sm text-primary-text-secondary font-bold uppercase">Vitesse Veille</span>
                      <span className="text-xs text-accent font-black">TEMPS RÉEL</span>
                   </div>
                </div>
                
                <div className="mt-8 p-6 bg-accent/5 border border-accent/20 rounded-2xl">
                   <p className="text-xs text-primary-text-secondary font-medium leading-relaxed">
                      Les alertes sont envoyées dès qu'une nouvelle annonce correspond à vos critères d'élite. 
                      <span className="block mt-2 text-white font-bold italic">"Soyez le premier sur le coup."</span>
                   </p>
                </div>
             </div>
          </div>
        </div>
      </div>

      {/* Overlay Form Modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#0D0D14]/90 backdrop-blur-md animate-fade-in">
           <div className="bg-primary-card border border-primary-border/DEFAULT w-full max-w-2xl rounded-[2.5rem] p-8 md:p-12 shadow-2xl relative overflow-y-auto max-h-[90vh]">
              <button 
                onClick={() => setShowForm(false)}
                className="absolute top-8 right-8 p-2 text-primary-text-secondary hover:text-white transition-colors"
              >
                <X size={24} />
              </button>

              <h2 className="text-3xl font-black text-white mb-8 pr-12">
                {editingId ? "Modifier l'Alerte" : "Créer une Nouvelle Alerte d'Élite"}
              </h2>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                   <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Nom de l'alerte</label>
                   <input 
                     required
                     placeholder="Ex: BMW Série 3 Prochain Coup"
                     className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-5 text-white outline-none focus:border-accent transition-all font-bold"
                     value={formData.titre}
                     onChange={e => setFormData({...formData, titre: e.target.value})}
                   />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Marque</label>
                    <input 
                      placeholder="Audi, BMW..."
                      className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-4 text-white outline-none focus:border-accent transition-all font-bold"
                      value={formData.marque}
                      onChange={e => setFormData({...formData, marque: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Modèle</label>
                    <input 
                      placeholder="A3, 308..."
                      className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-4 text-white outline-none focus:border-accent transition-all font-bold"
                      value={formData.modele}
                      onChange={e => setFormData({...formData, modele: e.target.value})}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Prix Max (€)</label>
                    <input 
                      type="number"
                      className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-4 text-white outline-none focus:border-accent transition-all font-bold"
                      value={formData.prix_max}
                      onChange={e => setFormData({...formData, prix_max: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Km Max</label>
                    <input 
                      type="number"
                      className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-4 text-white outline-none focus:border-accent transition-all font-bold"
                      value={formData.km_max}
                      onChange={e => setFormData({...formData, km_max: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Année Min</label>
                    <input 
                      type="number"
                      className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-4 text-white outline-none focus:border-accent transition-all font-bold"
                      value={formData.annee_min}
                      onChange={e => setFormData({...formData, annee_min: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Carburant</label>
                    <select 
                      className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-4 text-white outline-none focus:border-accent transition-all font-bold appearance-none cursor-pointer"
                      value={formData.carburant}
                      onChange={e => setFormData({...formData, carburant: e.target.value})}
                    >
                       <option value="">Tous</option>
                       <option value="essence">Essence</option>
                       <option value="diesel">Diesel</option>
                       <option value="electrique">Électrique</option>
                       <option value="hybride">Hybride</option>
                    </select>
                  </div>
                </div>

                <div className="bg-primary-elevated p-6 rounded-3xl border border-primary-border/DEFAULT space-y-4">
                  <p className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest mb-2">Canaux de Notification</p>
                  <div className="flex flex-col md:flex-row gap-6">
                    <label className="flex items-center gap-4 cursor-pointer group">
                       <input 
                         type="checkbox" 
                         className="hidden"
                         checked={formData.email_actif}
                         onChange={e => setFormData({...formData, email_actif: e.target.checked})}
                       />
                       <div className={`w-12 h-6 rounded-full transition-all relative ${formData.email_actif ? 'bg-accent' : 'bg-gray-700'}`}>
                          <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${formData.email_actif ? 'left-7' : 'left-1'}`}></div>
                       </div>
                       <span className="text-sm font-bold text-white group-hover:text-accent transition-colors">Alertes Email</span>
                    </label>
                    <label className="flex items-center gap-4 cursor-pointer group">
                       <input 
                         type="checkbox" 
                         className="hidden"
                         checked={formData.push_actif}
                         onChange={e => setFormData({...formData, push_actif: e.target.checked})}
                       />
                       <div className={`w-12 h-6 rounded-full transition-all relative ${formData.push_actif ? 'bg-accent' : 'bg-gray-700'}`}>
                          <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${formData.push_actif ? 'left-7' : 'left-1'}`}></div>
                       </div>
                       <span className="text-sm font-bold text-white group-hover:text-accent transition-colors">Alertes App (Push)</span>
                    </label>
                  </div>
                </div>

                <div className="pt-6 flex gap-4">
                  <button 
                    type="submit"
                    className="flex-1 bg-accent text-white py-5 rounded-2xl font-black text-lg hover:scale-[1.02] transition-all shadow-xl shadow-accent/20"
                  >
                    🚀 {editingId ? "Sauvegarder les modifications" : "Lancer la Veille d'Élite"}
                  </button>
                </div>
              </form>
           </div>
        </div>
      )}

      <style jsx>{`
        @keyframes slide-in {
          from { opacity: 0; transform: translateX(-20px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce-subtle {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-3px); }
        }
        .animate-slide-in { animation: slide-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .animate-fade-in { animation: fade-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .animate-bounce-subtle { animation: bounce-subtle 3s ease-in-out infinite; }
      `}</style>

    </div>
  );
}
