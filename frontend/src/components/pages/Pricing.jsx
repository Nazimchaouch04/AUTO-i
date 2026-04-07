import React, { useState, useEffect } from 'react';
import { Check, X, Zap, Crown, Building, ArrowRight, Loader2, ShieldCheck, Sparkles } from 'lucide-react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';

const API_BASE = '/api/subscriptions/';

export default function Pricing() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(null);
  const [error, setError] = useState(null);
  
  const { user, isAuthenticated } = useSelector(state => state.user);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await axiosClient.get(`${API_BASE}plans/`);
      const data = response.data;
      // Sort plans: Free, Pro, Business
      const order = { 'free': 0, 'pro': 1, 'business': 2 };
      const sorted = (data.results || data).sort((a, b) => order[a.nom] - order[b.nom]);
      setPlans(sorted);
    } catch (err) {
      setError("Impossible de charger les offres.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (planNom) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (user?.plan_nom === planNom) return;

    setUpgrading(planNom);
    setError(null);

    try {
      const response = await axiosClient.post(`${API_BASE}checkout/`, { plan: planNom });
      const data = response.data;

      if (data.url) {
        window.location.href = data.url;
      } else {
        setError(data.error || "Échec de la création du paiement.");
        setUpgrading(null);
      }
    } catch (err) {
      setError(err?.response?.data?.error || "Erreur lors de la création du paiement");
      setUpgrading(null);
    }
  };

  const currentPlan = user?.plan_nom || 'free';

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0D0D14] flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-accent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D14] pt-32 pb-20 px-4">
      <div className="max-w-7xl mx-auto text-center mb-20 animate-fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 rounded-full border border-accent/20 mb-6">
          <Sparkles className="w-4 h-4 text-accent" />
          <span className="text-xs font-black text-accent uppercase tracking-widest">Offres Limited Edition</span>
        </div>
        <h1 className="text-5xl md:text-7xl font-black text-white tracking-tighter mb-6">
          Passez Ã  la <span className="text-accent underline decoration-4 underline-offset-8">Vitesse SupÃ©rieure</span>
        </h1>
        <p className="text-xl text-primary-text-secondary max-w-2xl mx-auto">
          DÃ©bloquez la puissance d'AutoIntel et devenez le maÃ®tre du marchÃ© automobile.
        </p>
      </div>

      {error && (
        <div className="max-w-md mx-auto mb-10 p-4 bg-danger/10 border border-danger/20 rounded-2xl text-danger text-center font-bold">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {plans.map((plan) => (
          <div 
            key={plan.id}
            className={`relative group bg-primary-card border transition-all duration-500 rounded-[3rem] p-10 flex flex-col ${
              plan.nom === 'pro' 
                ? 'border-accent shadow-2xl shadow-accent/10 scale-105 z-10' 
                : 'border-primary-border/DEFAULT hover:border-white/20'
            }`}
          >
            {plan.nom === 'pro' && (
              <div className="absolute -top-5 left-1/2 -translate-x-1/2 bg-accent text-white text-[10px] font-black uppercase tracking-widest px-6 py-2 rounded-full shadow-lg">
                RecommandÃ©
              </div>
            )}

            <div className="mb-8">
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 ${
                plan.nom === 'free' ? 'bg-primary-elevated text-primary-text-secondary' :
                plan.nom === 'pro' ? 'bg-accent/10 text-accent' : 'bg-warning/10 text-warning'
              }`}>
                {plan.nom === 'free' ? <Zap size={28} /> :
                 plan.nom === 'pro' ? <Crown size={28} /> : <Building size={28} />}
              </div>
              <h3 className="text-2xl font-black text-white capitalize mb-2">{plan.nom}</h3>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-black text-white">{parseInt(plan.prix_mensuel)}â‚¬</span>
                <span className="text-primary-text-secondary font-medium">/mois</span>
              </div>
            </div>

            <div className="space-y-5 mb-10 flex-1">
              <FeatureItem active={true} text={`${plan.estimations_par_mois} Estimations / mois`} />
              <FeatureItem active={true} text={`${plan.alertes_max} Alertes Intelligentes`} />
              <FeatureItem active={plan.export_csv} text={plan.nom === 'free' ? 'Export CSV (Pro uniquement)' : 'Export CSV illimitÃ©'} />
              <FeatureItem active={plan.acces_api} text="AccÃ¨s API DÃ©veloppeur" />
              <FeatureItem active={plan.nom !== 'free'} text="Support Prioritaire 24/7" />
              <FeatureItem active={plan.nom === 'business'} text="AccÃ¨s Flotte & Garage" />
            </div>

            <button
              onClick={() => handleUpgrade(plan.nom)}
              disabled={upgrading !== null || currentPlan === plan.nom}
              className={`w-full py-5 rounded-2xl font-black text-sm uppercase tracking-widest transition-all flex items-center justify-center gap-3 ${
                currentPlan === plan.nom 
                  ? 'bg-success/10 text-success cursor-default border border-success/20' :
                plan.nom === 'pro'
                  ? 'bg-accent text-white hover:scale-[1.02] shadow-xl shadow-accent/20'
                  : 'bg-primary-elevated text-white hover:bg-white/10'
              }`}
            >
              {upgrading === plan.nom ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : currentPlan === plan.nom ? (
                <> <ShieldCheck size={20} /> Plan Actuel </>
              ) : (
                <> Choisir ce plan <ArrowRight size={18} /> </>
              )}
            </button>
          </div>
        ))}
      </div>

      <div className="mt-32 max-w-4xl mx-auto text-center bg-primary-card/50 border border-primary-border/DEFAULT rounded-[3rem] p-12 backdrop-blur-sm animate-fade-in-up">
        <h2 className="text-3xl font-black text-white mb-6">Besoin d'une solution sur-mesure ?</h2>
        <p className="text-primary-text-secondary mb-10 text-lg">
          Vous Ãªtes un concessionnaire ou gÃ©rez une flotte importante ? 
          Nos experts vous accompagnent avec des outils dÃ©diÃ©s.
        </p>
        <button className="px-10 py-5 bg-white text-black font-black rounded-2xl hover:scale-105 transition-all text-sm uppercase tracking-widest">
          Contacter les experts
        </button>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in { animation: fade-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .animate-fade-in-up { animation: fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
      `}</style>
    </div>
  );
}

function FeatureItem({ active, text }) {
  return (
    <div className={`flex items-center gap-3 text-sm ${active ? 'text-primary-text-primary' : 'text-primary-text-secondary line-through opacity-40'}`}>
      <div className={`w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 ${active ? 'bg-success/10 text-success' : 'bg-primary-elevated text-primary-text-secondary'}`}>
        {active ? <Check size={12} strokeWidth={4} /> : <X size={12} strokeWidth={4} />}
      </div>
      <span className="font-bold">{text}</span>
    </div>
  );
}


