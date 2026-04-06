import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, ArrowRight, Check, X, 
  Search, Gauge, Calendar, Zap, 
  MapPin, Fuel, Power, BarChart3,
  TrendingDown, TrendingUp, DollarSign
} from 'lucide-react';

const Comparison = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [vehicles, setVehicles] = useState({ v1: null, v2: null });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const v1_id = params.get('v1');
    const v2_id = params.get('v2');

    const fetchVehicles = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/annonces/versus/?v1=${v1_id}&v2=${v2_id}`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const data = await res.json();
        setVehicles({ v1: data.v1, v2: data.v2 });
      } catch (e) {
        console.error("Erreur comparaison:", e);
      } finally {
        setLoading(false);
      }
    };

    if (v1_id && v2_id) fetchVehicles();
  }, [location]);

  if (loading) return (
    <div className="min-h-screen bg-primary-bg flex justify-center items-center">
      <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full animate-spin" />
    </div>
  );

  const v1 = vehicles.v1;
  const v2 = vehicles.v2;

  const CompareRow = ({ label, val1, val2, inverse = false, suffix = "" }) => {
    const isBetter = inverse ? (val1 < val2) : (val1 > val2);
    const isEqual = val1 === val2;

    return (
      <tr className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
        <td className="py-5 px-6 text-xs font-bold text-primary-text-secondary uppercase tracking-widest">{label}</td>
        <td className={`py-5 px-6 text-center ${isBetter ? 'text-accent font-black' : 'text-white'}`}>
           {val1.toLocaleString()}{suffix}
           {isBetter && !isEqual && <TrendingUp className="inline ml-2" size={14} />}
        </td>
        <td className={`py-5 px-6 text-center ${(!isBetter && !isEqual) ? 'text-accent font-black' : 'text-white'}`}>
           {val2.toLocaleString()}{suffix}
           {(!isBetter && !isEqual) && <TrendingUp className="inline ml-2" size={14} />}
        </td>
      </tr>
    );
  };

  return (
    <div className="min-h-screen bg-[#0A0A0F] pt-24 pb-20 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        <button 
          onClick={() => navigate(-1)}
          className="mb-8 flex items-center gap-2 text-primary-text-secondary hover:text-white transition-colors"
        >
          <ArrowLeft size={18} /> Retour
        </button>

        <div className="mb-16">
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight">Analyse Comparative</h1>
          <p className="text-primary-text-secondary">Confrontation technique assistée par l'IA.</p>
        </div>

        {/* Comparison Table */}
        <div className="overflow-hidden rounded-[2.5rem] border border-primary-border/DEFAULT bg-primary-card shadow-2xl">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-white/[0.03]">
                <th className="py-10 px-6 text-left">
                   <div className="flex items-center gap-2 text-accent">
                      <BarChart3 size={20} />
                      <span className="text-[10px] font-black uppercase tracking-[0.2em] opacity-60">Specifications</span>
                   </div>
                </th>
                <th className="py-10 px-6">
                   <div className="text-center">
                      <p className="text-xl font-black text-white">{v1.vehicule_marque}</p>
                      <p className="text-xs text-accent">{v1.vehicule_modele}</p>
                   </div>
                </th>
                <th className="py-10 px-6">
                   <div className="text-center">
                      <p className="text-xl font-black text-white">{v2.vehicule_marque}</p>
                      <p className="text-xs text-accent">{v2.vehicule_modele}</p>
                   </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <CompareRow label="Prix" val1={v1.prix} val2={v2.prix} inverse suffix="€" />
              <CompareRow label="Année" val1={v1.annee} val2={v2.annee} />
              <CompareRow label="Kilométrage" val1={v1.kilometrage} val2={v2.kilometrage} inverse suffix=" km" />
              <CompareRow label="Score Affaire" val1={v1.score_affaire} val2={v2.score_affaire} suffix="/100" />
              <CompareRow label="Puissance" val1={v1.puissance || 0} val2={v2.puissance || 0} suffix=" ch" />
              
              {/* Boolean Rows */}
              <tr className="border-b border-white/5">
                <td className="py-5 px-6 text-xs font-bold text-primary-text-secondary uppercase">Boite Automatique</td>
                <td className="py-5 px-6 text-center">{v1.boite === 'automatique' ? <Check className="mx-auto text-success" /> : <X className="mx-auto text-danger opacity-30" />}</td>
                <td className="py-5 px-6 text-center">{v2.boite === 'automatique' ? <Check className="mx-auto text-success" /> : <X className="mx-auto text-danger opacity-30" />}</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="py-5 px-6 text-xs font-bold text-primary-text-secondary uppercase">Bonne Affaire</td>
                <td className="py-5 px-6 text-center">{v1.est_bonne_affaire ? <Zap className="mx-auto text-yellow-500 fill-yellow-500" /> : <X className="mx-auto text-danger opacity-30" />}</td>
                <td className="py-5 px-6 text-center">{v2.est_bonne_affaire ? <Zap className="mx-auto text-yellow-500 fill-yellow-500" /> : <X className="mx-auto text-danger opacity-30" />}</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Verdict Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
           <div className="p-8 bg-blue-500/5 border border-blue-500/20 rounded-3xl">
              <div className="flex items-center gap-3 mb-6">
                 <DollarSign className="text-blue-500" size={24} />
                 <h4 className="text-xl font-bold text-white">Économie Potentielle</h4>
              </div>
              <p className="text-primary-text-secondary text-sm">
                En choisissant le {v1.prix < v2.prix ? v1.vehicule_marque : v2.vehicule_marque}, 
                vous économisez <span className="text-blue-400 font-bold">{Math.abs(v1.prix - v2.prix).toLocaleString()}€</span> immédiatement.
              </p>
           </div>
           <div className="p-8 bg-accent/5 border border-accent/20 rounded-3xl">
              <div className="flex items-center gap-3 mb-6">
                 <Zap className="text-accent" size={24} />
                 <h4 className="text-xl font-bold text-white">Recommandation IA</h4>
              </div>
              <p className="text-primary-text-secondary text-sm">
                Basé sur le score d'affaire de {v1.score_affaire > v2.score_affaire ? v1.score_affaire : v2.score_affaire}, 
                le <span className="text-accent font-bold">{v1.score_affaire > v2.score_affaire ? v1.vehicule_marque : v2.vehicule_marque}</span> est le choix le plus rationnel.
              </p>
           </div>
        </div>
      </div>
    </div>
  );
};

export default Comparison;
