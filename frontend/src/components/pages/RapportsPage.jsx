import React, { useState, useEffect } from 'react';
import {
  FileText, Download, Plus, CreditCard, Eye, Trash2,
  Clock, CheckCircle, AlertCircle, TrendingUp, BarChart3,
  Filter, Search, Calendar, DollarSign, Zap, X
} from 'lucide-react';
import PageTransition from '../ui/PageTransition';
import EmptyState from '../ui/EmptyState';
import { useToast } from '../ui/Toast';
import axiosClient from '../../api/axiosClient';

const API_BASE = '/api/rapports/';

export default function RapportsPage() {
  const [rapports, setRapports] = useState([]);
  const [typesRapports, setTypesRapports] = useState([]);
  const [statistiques, setStatistiques] = useState({});
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedType, setSelectedType] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);
  const { showToast } = useToast();

  const [formData, setFormData] = useState({
    titre: '',
    type_rapport: '',
    annonce_principale_id: '',
    annonces_comparees: [],
    alerte_source_id: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [rapportsResponse, typesResponse, statsResponse] = await Promise.all([
        axiosClient.get(API_BASE),
        axiosClient.get(`${API_BASE}types/`),
        axiosClient.get(`${API_BASE}statistiques/`)
      ]);

      setRapports(rapportsResponse.data || []);
      setTypesRapports(typesResponse.data || []);
      setStatistiques(statsResponse.data || {});
    } catch (err) {
      setError("Impossible de charger les rapports.");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRapport = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axiosClient.post(`${API_BASE}creer/`, formData);
      const data = response.data;

      showToast({ message: "Rapport créé avec succès", type: 'success' });
      setShowCreateForm(false);
      setSelectedType('');
      resetForm();
      fetchData();

      // Redirige vers le paiement si nécessaire
      if (data.statut_paiement === 'en_attente') {
        handlePayment(data.id);
      }
    } catch (err) {
      setError(err?.response?.data?.error || "Une erreur est survenue.");
    }
  };

  const handlePayment = async (rapportId) => {
    try {
      const response = await axiosClient.post(`${API_BASE}${rapportId}/payer/`);
      const data = response.data;

      // Utiliser Stripe Elements pour le paiement
      // Pour l'instant, on montre les informations
      showToast({
        message: `Paiement de ${data.prix}€ à confirmer`,
        type: 'info'
      });
    } catch (err) {
      setError(err?.response?.data?.error || "Erreur de paiement.");
    }
  };

  const handleDownload = async (rapportId) => {
    try {
      const response = await axiosClient.get(`${API_BASE}${rapportId}/telecharger/`, {
        responseType: 'blob'
      });

      const blob = response.data;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `rapport_${rapportId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      showToast({ message: "Rapport téléchargé", type: 'success' });
    } catch (err) {
      setError(err?.response?.data?.error || "Erreur de téléchargement.");
    }
  };

  const handleDelete = async (rapportId) => {
    if (!window.confirm("Supprimer ce rapport ?")) return;

    try {
      await axiosClient.delete(`${API_BASE}${rapportId}/supprimer/`);

      setRapports(prev => prev.filter(r => r.id !== rapportId));
      showToast({ message: "Rapport supprimé", type: 'success' });
      fetchData();
    } catch (err) {
      setError("Erreur de suppression.");
    }
  };

  const resetForm = () => {
    setFormData({
      titre: '',
      type_rapport: '',
      annonce_principale_id: '',
      annonces_comparees: [],
      alerte_source_id: '',
    });
  };

  const getTypeInfo = (type) => {
    return typesRapports.find(t => t.type === type) || {};
  };

  const getStatusColor = (statut) => {
    switch (statut) {
      case 'termine': return 'text-success';
      case 'en_attente': return 'text-warning';
      case 'generation': return 'text-blue-500';
      case 'erreur': return 'text-danger';
      default: return 'text-primary-text-secondary';
    }
  };

  const getStatusIcon = (statut) => {
    switch (statut) {
      case 'termine': return <CheckCircle size={16} />;
      case 'en_attente': return <Clock size={16} />;
      case 'generation': return <Zap size={16} />;
      case 'erreur': return <AlertCircle size={16} />;
      default: return <Clock size={16} />;
    }
  };

  const filteredRapports = rapports.filter(rapport =>
    rapport.titre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    rapport.type_display.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <PageTransition>
      <div className="min-h-screen bg-[#0D0D14] pt-28 pb-20 px-4 md:px-8">
        <div className="max-w-7xl mx-auto">
          
          {/* Header Section */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
            <div className="animate-slide-in">
              <h1 className="text-4xl font-black text-white tracking-tight mb-2 flex items-center gap-3">
                 <FileText className="text-accent" size={36} />
                 Rapports <span className="text-accent">PDF</span>
              </h1>
              <p className="text-primary-text-secondary">Analysez le marchÃ© automobile en dÃ©tail.</p>
            </div>
            <button 
              onClick={() => { resetForm(); setShowCreateForm(true); }}
              className="bg-accent text-white px-8 py-4 rounded-2xl font-bold flex items-center justify-center gap-3 hover:scale-105 transition-all shadow-xl shadow-accent/20"
            >
              <Plus size={20} />
              Nouveau Rapport
            </button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-primary-text-secondary font-bold uppercase">Total Rapports</p>
                  <p className="text-2xl font-black text-white">{statistiques.total_rapports || 0}</p>
                </div>
                <div className="w-12 h-12 bg-blue-500/20 rounded-2xl flex items-center justify-center">
                  <FileText className="text-blue-400" size={24} />
                </div>
              </div>
            </div>

            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-primary-text-secondary font-bold uppercase">PayÃ©s</p>
                  <p className="text-2xl font-black text-white">{statistiques.rapports_payes || 0}</p>
                </div>
                <div className="w-12 h-12 bg-green-500/20 rounded-2xl flex items-center justify-center">
                  <CheckCircle className="text-green-400" size={24} />
                </div>
              </div>
            </div>

            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-primary-text-secondary font-bold uppercase">En Attente</p>
                  <p className="text-2xl font-black text-white">{statistiques.rapports_en_attente || 0}</p>
                </div>
                <div className="w-12 h-12 bg-yellow-500/20 rounded-2xl flex items-center justify-center">
                  <Clock className="text-yellow-400" size={24} />
                </div>
              </div>
            </div>

            <div className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-primary-text-secondary font-bold uppercase">Total DÃ©pensÃ©</p>
                  <p className="text-2xl font-black text-white">{(statistiques.total_depense || 0).toFixed(2)}â‚¬</p>
                </div>
                <div className="w-12 h-12 bg-purple-500/20 rounded-2xl flex items-center justify-center">
                  <DollarSign className="text-purple-400" size={24} />
                </div>
              </div>
            </div>
          </div>

          {/* Search and Filter */}
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-primary-text-secondary" size={20} />
              <input
                type="text"
                placeholder="Rechercher un rapport..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl pl-12 pr-4 py-4 text-white outline-none focus:border-accent transition-all font-bold"
              />
            </div>
          </div>

          {error && (
            <div className="mb-8 p-4 bg-danger/10 border border-danger/20 rounded-2xl flex items-center gap-3 text-danger animate-bounce-subtle">
               <AlertCircle size={20} />
               <p className="font-bold text-sm">{error}</p>
               <button onClick={() => setError(null)} className="ml-auto"><X size={18} /></button>
            </div>
          )}

          {/* Rapports List */}
          <div className="space-y-6">
            {loading ? (
              [1, 2, 3].map(n => <div key={n} className="h-40 bg-primary-card rounded-3xl animate-pulse border border-primary-border/DEFAULT" />)
            ) : filteredRapports.length > 0 ? (
              filteredRapports.map(rapport => (
                <div key={rapport.id} className="bg-primary-card border border-primary-border/DEFAULT rounded-3xl p-6 md:p-8 hover:border-accent/50 transition-all duration-300">
                  
                  <div className="flex flex-col md:flex-row gap-6">
                    <div className="w-16 h-16 bg-accent/10 rounded-2xl flex items-center justify-center">
                       <FileText className="text-accent" size={32} />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-bold text-white">{rapport.titre}</h3>
                        <span className="px-3 py-1 bg-primary-elevated text-xs font-bold text-primary-text-secondary rounded-full">
                          {rapport.type_display}
                        </span>
                      </div>
                      
                      <div className="flex flex-wrap gap-4 text-sm text-primary-text-secondary mb-4">
                        <span className="flex items-center gap-1">
                          {getStatusIcon(rapport.statut_paiement)}
                          <span className={getStatusColor(rapport.statut_paiement)}>
                            {rapport.statut_display}
                          </span>
                        </span>
                        <span>CrÃ©Ã© le {new Date(rapport.created_at).toLocaleDateString()}</span>
                        {rapport.genere_at && (
                          <span>GÃ©nÃ©rÃ© le {new Date(rapport.genere_at).toLocaleDateString()}</span>
                        )}
                        <span className="font-bold text-accent">{rapport.prix}â‚¬</span>
                      </div>

                      {rapport.annonce && (
                        <div className="text-sm text-primary-text-secondary">
                          VÃ©hicule : {rapport.annonce.titre}
                        </div>
                      )}
                    </div>

                    <div className="flex md:flex-col justify-end gap-2">
                       {rapport.statut_paiement === 'en_attente' && (
                         <button 
                           onClick={() => handlePayment(rapport.id)}
                           className="p-3 bg-warning/10 text-warning rounded-2xl hover:bg-warning/20 transition-all"
                           title="Payer"
                         >
                           <CreditCard size={20} />
                         </button>
                       )}
                       {rapport.peut_etre_telecharge && (
                         <button 
                           onClick={() => handleDownload(rapport.id)}
                           className="p-3 bg-success/10 text-success rounded-2xl hover:bg-success/20 transition-all"
                           title="TÃ©lÃ©charger"
                         >
                           <Download size={20} />
                         </button>
                       )}
                       <button 
                         onClick={() => window.open(`/rapports/${rapport.id}`, '_blank')}
                         className="p-3 bg-primary-elevated text-white rounded-2xl hover:bg-accent/20 hover:text-accent transition-all"
                         title="Voir dÃ©tails"
                       >
                         <Eye size={20} />
                       </button>
                       <button 
                         onClick={() => handleDelete(rapport.id)}
                         className="p-3 bg-danger/10 text-danger rounded-2xl hover:bg-danger/20 transition-all"
                         title="Supprimer"
                       >
                         <Trash2 size={20} />
                       </button>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="col-span-full">
                <EmptyState 
                  icon="ðŸ“„" 
                  title="Aucun rapport crÃ©Ã©" 
                  subtitle="GÃ©nÃ©rez votre premier rapport PDF pour analyser le marchÃ©" 
                  actionLabel="CrÃ©er un rapport" 
                  onAction={() => { resetForm(); setShowCreateForm(true); }}
                />
              </div>
            )}
          </div>
        </div>

        {/* Create Form Modal */}
        {showCreateForm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#0D0D14]/90 backdrop-blur-md animate-fade-in">
             <div className="bg-primary-card border border-primary-border/DEFAULT w-full max-w-2xl rounded-[2.5rem] p-8 md:p-12 shadow-2xl relative overflow-y-auto max-h-[90vh]">
                <button 
                  onClick={() => setShowCreateForm(false)}
                  className="absolute top-8 right-8 p-2 text-primary-text-secondary hover:text-white transition-colors"
                >
                  <X size={24} />
                </button>

                <h2 className="text-3xl font-black text-white mb-8 pr-12">
                  CrÃ©er un Nouveau Rapport
                </h2>

                {/* Type Selection */}
                {!selectedType ? (
                  <div className="space-y-4">
                    <p className="text-sm text-primary-text-secondary font-medium mb-6">
                      Choisissez le type de rapport que vous souhaitez gÃ©nÃ©rer :
                    </p>
                    {typesRapports.map(type => (
                      <button
                        key={type.type}
                        onClick={() => {
                          setSelectedType(type.type);
                          setFormData({...formData, type_rapport: type.type});
                        }}
                        className="w-full p-6 bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl hover:border-accent/50 transition-all text-left"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h3 className="text-lg font-bold text-white mb-2">{type.nom}</h3>
                            <p className="text-sm text-primary-text-secondary">{type.description}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-xl font-black text-accent">{type.prix}</p>
                            <p className="text-xs text-primary-text-secondary">{type.delai}</p>
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                ) : (
                  <form onSubmit={handleCreateRapport} className="space-y-6">
                    <div className="space-y-2">
                       <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Titre du rapport</label>
                       <input 
                         required
                         placeholder="Ex: Analyse BMW SÃ©rie 3 2020"
                         className="w-full bg-primary-elevated border border-primary-border/DEFAULT rounded-2xl p-5 text-white outline-none focus:border-accent transition-all font-bold"
                         value={formData.titre}
                         onChange={e => setFormData({...formData, titre: e.target.value})}
                       />
                    </div>

                    <div className="space-y-2">
                       <label className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest pl-2">Type de rapport</label>
                       <div className="p-4 bg-primary-elevated rounded-2xl">
                         <p className="text-white font-bold">{getTypeInfo(formData.type_rapport).nom}</p>
                         <p className="text-sm text-primary-text-secondary">{getTypeInfo(formData.type_rapport).description}</p>
                         <p className="text-lg font-black text-accent mt-2">{getTypeInfo(formData.type_rapport).prix}</p>
                       </div>
                    </div>

                    <div className="flex gap-4">
                      <button
                        type="button"
                        onClick={() => setSelectedType('')}
                        className="flex-1 bg-primary-elevated text-white py-4 rounded-2xl font-bold hover:bg-gray-700 transition-all"
                      >
                        Retour
                      </button>
                      <button
                        type="submit"
                        className="flex-1 bg-accent text-white py-4 rounded-2xl font-bold hover:scale-[1.02] transition-all shadow-xl shadow-accent/20"
                      >
                        CrÃ©er et Payer {getTypeInfo(formData.type_rapport).prix}
                      </button>
                    </div>
                  </form>
                )}
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
    </PageTransition>
  );
}

