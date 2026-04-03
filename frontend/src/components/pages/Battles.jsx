import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Swords, Trophy, Users, Zap, ArrowRight, Flame } from 'lucide-react';

const Battles = () => {
  const [battles, setBattles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBattles = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/annonces/battles/', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const data = await response.json();
        setBattles(data);
      } catch (e) {
        console.error("Erreur battles:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchBattles();
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-primary-bg flex items-center justify-center pt-20">
      <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="min-h-screen bg-[#08080C] pt-24 pb-20 px-4 md:px-8 relative">
       {/* Background Glows */}
       <div className="absolute top-0 left-1/4 w-96 h-96 bg-accent/10 rounded-full blur-[120px]" />
       <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-[120px]" />

       <div className="max-w-7xl mx-auto relative z-10">
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
             <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 bg-accent/10 border border-accent/20 rounded-full text-accent text-[10px] font-black uppercase tracking-widest mb-6">
                   <Flame size={14} className="animate-pulse" />
                   Live Arena
                </div>
                <h1 className="text-4xl md:text-6xl font-black text-white tracking-tighter uppercase line-height-[0.9]">
                   Vehicle <span className="text-accent underline decoration-white/10 underline-offset-8">Battles</span>
                </h1>
             </div>
             <p className="text-primary-text-secondary max-w-md text-right text-sm md:text-base">
                Votez pour les meilleures affaires du moment et gagnez des AutoCoins. 
                Les duels sont arbitrés par nos algorithmes de marché.
             </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
             {battles.map((battle) => (
                <Link 
                  key={battle.id}
                  to={`/battle/${battle.id}`}
                  className="group bg-primary-card border border-white/5 rounded-[2.5rem] p-1 overflow-hidden transition-all hover:border-accent/50 hover:shadow-[0_0_50px_rgba(0,180,216,0.1)]"
                >
                   <div className="bg-[#0D0D14] rounded-[2.3rem] p-8 h-full flex flex-col">
                      <div className="flex justify-between items-start mb-8">
                         <span className="text-[10px] font-bold text-primary-text-secondary uppercase tracking-widest bg-white/5 px-3 py-1 rounded-full">
                            ID #{battle.id}
                         </span>
                         <div className="flex -space-x-3">
                            <div className="w-8 h-8 rounded-full border-2 border-[#0D0D14] bg-accent flex items-center justify-center text-[10px] text-white font-bold">V</div>
                            <div className="w-8 h-8 rounded-full border-2 border-[#0D0D14] bg-purple-500 flex items-center justify-center text-[10px] text-white font-bold">S</div>
                         </div>
                      </div>

                      <h3 className="text-2xl font-black text-white mb-2 group-hover:text-accent transition-colors">
                         {battle.vehicule_1_details.vehicule_marque} <span className="text-white/30 text-lg mx-2">vs</span> {battle.vehicule_2_details.vehicule_marque}
                      </h3>
                      <p className="text-xs text-primary-text-secondary mb-8 font-medium">
                         {battle.vehicule_1_details.vehicule_modele} contre {battle.vehicule_2_details.vehicule_modele}
                      </p>

                      <div className="mt-auto">
                         <div className="flex justify-between items-center mb-4">
                            <div className="flex items-center gap-2 text-primary-text-secondary">
                               <Users size={14} />
                               <span className="text-xs font-bold text-white">{battle.votes_v1 + battle.votes_v2} votes</span>
                            </div>
                            <div className="text-xs font-bold text-success uppercase tracking-widest">+5 AC</div>
                         </div>
                         
                         <div className="flex gap-1 h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full bg-accent" style={{ width: `${(battle.votes_v1 / (battle.votes_v1 + battle.votes_v2 || 1)) * 100}%` }} />
                            <div className="h-full bg-purple-500" style={{ width: `${(battle.votes_v2 / (battle.votes_v1 + battle.votes_v2 || 1)) * 100}%` }} />
                         </div>

                         <div className="mt-8 flex items-center justify-between">
                            <span className="text-[10px] font-black text-primary-text-secondary uppercase tracking-[0.2em]">Entrer dans l'arène</span>
                            <div className="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-white group-hover:bg-accent group-hover:scale-110 transition-all">
                               <ArrowRight size={18} />
                            </div>
                         </div>
                      </div>
                   </div>
                </Link>
             ))}

             {/* Placeholder for creating a battle */}
             <div className="bg-dashed border-2 border-white/5 border-dashed rounded-[2.5rem] p-12 flex flex-col items-center justify-center text-center opacity-40 hover:opacity-100 transition-opacity">
                <Swords size={40} className="text-accent mb-6" />
                <h4 className="text-lg font-bold text-white mb-2">Pas de duel inspirant ?</h4>
                <p className="text-sm text-primary-text-secondary mb-6">Explorez les annonces et créez votre propre duel pour gagner +10 AC.</p>
                <Link to="/annonces" className="text-xs font-black text-accent uppercase tracking-widest hover:underline">
                   Voir les annonces
                </Link>
             </div>
          </div>
       </div>
    </div>
  );
};

export default Battles;
