import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Swords, TrendingUp, Gauge, Calendar, 
  CheckCircle2, AlertCircle, Share2, 
  Trophy, User, Timer, Zap, Coins 
} from 'lucide-react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProfile } from '../../store/userSlice';
import axiosClient from '../../api/axiosClient';

const Battle = () => {
  const { id } = useParams();
  const [battle, setBattle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isVoting, setIsVoting] = useState(false);
  const [hasVoted, setHasVoted] = useState(false);
  
  const { profil } = useSelector(state => state.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBattle = async () => {
      try {
        const response = await axiosClient.get(`/api/annonces/battles/${id}/`);
        const data = response.data;
        setBattle(data);
      } catch (e) {
        console.error("Erreur battle:", e);
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchBattle();
  }, [id]);

  const handleVote = async (vehiculeId) => {
    if (hasVoted || isVoting) return;
    setIsVoting(true);
    try {
      const response = await axiosClient.post(`/api/annonces/battles/${id}/vote/`, {
        vehicule_id: vehiculeId
      });
      const data = response.data;
      setBattle(prev => ({ ...prev, votes_v1: data.votes_v1, votes_v2: data.votes_v2 }));
      setHasVoted(true);
      dispatch(fetchProfile()); // Refresh coins
    } catch (e) {
      console.error(e);
    } finally { setIsVoting(false); }
  };

  if (loading) return (
    <div className="min-h-screen bg-primary-bg flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!battle) return <div>Battle non trouvÃ©e</div>;

  const v1 = battle.vehicule_1_details;
  const v2 = battle.vehicule_2_details;
  const totalVotes = battle.votes_v1 + battle.votes_v2;
  const pctV1 = totalVotes === 0 ? 50 : Math.round((battle.votes_v1 / totalVotes) * 100);
  const pctV2 = 100 - pctV1;

  return (
    <div className="min-h-screen bg-[#08080C] pt-24 pb-20 px-4 md:px-8 relative overflow-hidden">
      {/* Background FX */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-gradient-to-b from-accent/10 to-transparent blur-3xl opacity-30" />
      <div className="absolute top-[20%] left-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl" />
      <div className="absolute top-[20%] right-0 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl" />

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header Battle */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-3 px-6 py-2 bg-white/5 border border-white/10 rounded-full text-white text-xs font-bold uppercase tracking-[0.3em] mb-8">
            <Swords size={18} className="text-accent" />
            Arena Duel
          </div>
          <h1 className="text-4xl md:text-7xl font-black text-white mb-6 uppercase tracking-tighter">
            The Great <span className="text-accent">Showdown</span>
          </h1>
          <p className="text-primary-text-secondary max-w-xl mx-auto">
            {battle.titre || "Duel d'Ã©lite entre deux bÃªtes de la route. Qui mÃ©rite votre vote ?"}
          </p>
        </div>

        {/* VS Interface */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] items-center gap-8 mb-20">
          
          {/* VÃ©hicule 1 */}
          <div className={`relative transition-all duration-700 ${hasVoted ? (battle.votes_v1 >= battle.votes_v2 ? 'scale-105' : 'opacity-70 grayscale-[0.5]') : ''}`}>
             <div className="bg-primary-card border-2 border-accent/20 rounded-[3rem] p-8 relative overflow-hidden group">
                <div className="absolute -left-10 -top-10 w-40 h-40 bg-accent/10 rounded-full blur-3xl" />
                <div className="relative z-10">
                  <div className="flex justify-between items-start mb-8">
                    <span className="px-4 py-1 bg-accent text-white text-[10px] font-black rounded-lg uppercase">Challenger A</span>
                    <div className="text-right">
                       <p className="text-3xl font-black text-white">{v1.prix.toLocaleString()}â‚¬</p>
                       <p className="text-xs text-primary-text-secondary">Prix de marchÃ©</p>
                    </div>
                  </div>
                  <h3 className="text-3xl font-black text-white mb-2">{v1.vehicule_marque}</h3>
                  <h4 className="text-xl font-bold text-accent mb-6">{v1.vehicule_modele}</h4>
                  
                  <div className="space-y-4 mb-10">
                    <StatRow icon={<Gauge size={16}/>} label="KM" value={v1.kilometrage.toLocaleString()} />
                    <StatRow icon={<Calendar size={16}/>} label="AnnÃ©e" value={v1.annee} />
                    <StatRow icon={<Zap size={16}/>} label="Score" value={`${v1.score_affaire}/100`} highlight />
                  </div>

                  <button 
                    onClick={() => handleVote(v1.id)}
                    disabled={hasVoted}
                    className={`w-full py-5 rounded-2xl font-black text-sm uppercase tracking-widest transition-all ${
                      hasVoted 
                        ? 'bg-primary-elevated text-primary-text-secondary' 
                        : 'bg-white text-black hover:bg-accent hover:text-white group-hover:scale-105'
                    }`}
                  >
                    {hasVoted ? `${pctV1}% des votes` : 'Voter pour Blue'}
                  </button>
                </div>
             </div>
          </div>

          {/* VS Center */}
          <div className="flex flex-col items-center gap-6">
             <div className="w-20 h-20 bg-accent rounded-full flex items-center justify-center text-white text-3xl font-black shadow-2xl shadow-accent/50 ring-8 ring-accent/20 animate-pulse">
                VS
             </div>
             <div className="w-[2px] h-32 bg-gradient-to-b from-accent to-transparent" />
          </div>

          {/* VÃ©hicule 2 */}
          <div className={`relative transition-all duration-700 ${hasVoted ? (battle.votes_v2 >= battle.votes_v1 ? 'scale-105' : 'opacity-70 grayscale-[0.5]') : ''}`}>
             <div className="bg-primary-card border-2 border-primary-border/20 rounded-[3rem] p-8 relative overflow-hidden group">
                <div className="absolute -right-10 -top-10 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl" />
                <div className="relative z-10">
                  <div className="flex justify-between items-start mb-8">
                    <span className="px-4 py-1 bg-primary-elevated text-white text-[10px] font-black rounded-lg uppercase">Challenger B</span>
                    <div className="text-right">
                       <p className="text-3xl font-black text-white">{v2.prix.toLocaleString()}â‚¬</p>
                       <p className="text-xs text-primary-text-secondary">Prix de marchÃ©</p>
                    </div>
                  </div>
                  <h3 className="text-3xl font-black text-white mb-2">{v2.vehicule_marque}</h3>
                  <h4 className="text-xl font-bold text-accent mb-6">{v2.vehicule_modele}</h4>
                  
                  <div className="space-y-4 mb-10">
                    <StatRow icon={<Gauge size={16}/>} label="KM" value={v2.kilometrage.toLocaleString()} />
                    <StatRow icon={<Calendar size={16}/>} label="AnnÃ©e" value={v2.annee} />
                    <StatRow icon={<Zap size={16}/>} label="Score" value={`${v2.score_affaire}/100`} highlight />
                  </div>

                  <button 
                    onClick={() => handleVote(v2.id)}
                    disabled={hasVoted}
                    className={`w-full py-5 rounded-2xl font-black text-sm uppercase tracking-widest transition-all ${
                      hasVoted 
                        ? 'bg-primary-elevated text-primary-text-secondary' 
                        : 'bg-white text-black hover:bg-accent hover:text-white group-hover:scale-105'
                    }`}
                  >
                    {hasVoted ? `${pctV2}% des votes` : 'Voter pour Red'}
                  </button>
                </div>
             </div>
          </div>

        </div>

        {/* Comparison Bar (Visible after vote) */}
        {hasVoted && (
          <div className="max-w-4xl mx-auto mb-20 animate-fade-in">
             <div className="flex justify-between mb-4 text-xs font-black text-white uppercase tracking-widest">
                <span>{battle.votes_v1} votes</span>
                <span>Tendance communautaire</span>
                <span>{battle.votes_v2} votes</span>
             </div>
             <div className="h-4 bg-primary-elevated rounded-full overflow-hidden flex shadow-2xl p-1">
                <div 
                  className="h-full bg-accent rounded-full transition-all duration-1000" 
                  style={{ width: `${pctV1}%` }} 
                />
                <div 
                  className="h-full bg-primary-text-secondary opacity-30 transition-all duration-1000" 
                  style={{ width: `${pctV2}%` }} 
                />
             </div>
          </div>
        )}

        {/* Verdict AutoIntel */}
         <div className="max-w-4xl mx-auto p-12 bg-gradient-to-r from-accent/10 to-accent-secondary/10 border border-accent/20 rounded-[3.5rem] relative overflow-hidden group">
            <Trophy className="absolute -right-10 -bottom-10 text-accent/10 group-hover:scale-110 transition-transform" size={200} />
            <div className="relative z-10 text-center md:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-accent text-white text-[10px] font-black rounded-full uppercase mb-6">
                 Expert Choice
              </div>
              <h2 className="text-3xl md:text-5xl font-black text-white mb-6 tracking-tight">Verdict AutoIntel</h2>
              <p className="text-primary-text-secondary text-lg mb-10 max-w-2xl">
                 Nos algorithmes ont analysÃ© plus de 5,000 annonces similaires. Le gagnant technique basÃ© sur la dÃ©cote, la raretÃ© et l'Ã©tat gÃ©nÃ©ral est :
              </p>
              
              <div className="flex flex-col md:flex-row items-center gap-8">
                 <div className="flex-1 p-8 bg-black/40 backdrop-blur-md rounded-3xl border border-white/5">
                    <h4 className="text-accent font-black text-2xl mb-1">
                       {battle.winner_id === v1.id ? v1.vehicule_marque : v2.vehicule_marque}
                    </h4>
                    <p className="text-white font-bold opacity-60">
                       {battle.winner_id === v1.id ? v1.vehicule_modele : v2.vehicule_modele}
                    </p>
                 </div>
                 <div className="flex flex-wrap justify-center gap-4">
                    <div className="flex flex-col items-center">
                       <span className="text-2xl font-black text-white">+{Math.abs(v1.score_affaire - v2.score_affaire)}</span>
                       <span className="text-[10px] font-bold text-primary-text-secondary uppercase">Diff. Score</span>
                    </div>
                 </div>
              </div>
            </div>
         </div>
      </div>
    </div>
  );
};

const StatRow = ({ icon, label, value, highlight }) => (
  <div className="flex items-center justify-between p-4 bg-black/20 rounded-2xl border border-white/5">
    <div className="flex items-center gap-3">
      <div className="text-accent opacity-70">{icon}</div>
      <span className="text-xs font-bold text-primary-text-secondary uppercase">{label}</span>
    </div>
    <span className={`font-black ${highlight ? 'text-accent text-lg' : 'text-white'}`}>{value}</span>
  </div>
);

export default Battle;

