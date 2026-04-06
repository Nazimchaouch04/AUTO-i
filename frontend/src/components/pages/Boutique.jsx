import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { 
  ShoppingBag, Zap, Award, Palette, CheckCircle2, 
  AlertCircle, ArrowRight, Coins, ShieldCheck,
  Star, Sparkles, Loader2, Lock
} from 'lucide-react';
import { fetchProfile } from '../../store/userSlice';

const Boutique = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [buyingId, setBuyingId] = useState(null);
  const [message, setMessage] = useState({ text: '', type: '' });
  
  const { profil } = useSelector(state => state.user);
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/gamification/shop/', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const data = await response.json();
        setItems(data.results || data);
      } catch (e) {
        console.error("Erreur boutique:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchItems();
  }, []);

  const handleBuy = async (itemId, itemNom) => {
    setBuyingId(itemId);
    setMessage({ text: '', type: '' });
    
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/gamification/shop/${itemId}/buy/`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setMessage({ text: `Succès ! Vous avez débloqué : ${itemNom}`, type: 'success' });
        dispatch(fetchProfile()); // Update balance in header
      } else {
        setMessage({ text: data.detail || "Erreur lors de l'achat", type: 'error' });
      }
    } catch (e) {
      setMessage({ text: "Erreur réseau", type: 'error' });
    } finally {
      setBuyingId(null);
      setTimeout(() => setMessage({ text: '', type: '' }), 5000);
    }
  };

  const getIcon = (slug) => {
    if (slug.includes('xp')) return <Zap size={24} />;
    if (slug.includes('badge')) return <Award size={24} />;
    if (slug.includes('theme')) return <Palette size={24} />;
    return <ShoppingBag size={24} />;
  };

  return (
    <div className="min-h-screen bg-[#060609] pt-24 pb-20 px-4 md:px-8">
      {/* Header Boutique */}
      <div className="max-w-7xl mx-auto mb-12 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 border border-accent/20 rounded-full text-accent text-xs font-bold uppercase tracking-widest mb-6 animate-fade-in">
          <Sparkles size={14} />
          Boutique AutoIntel
        </div>
        <h1 className="text-4xl md:text-6xl font-black text-white mb-6 tracking-tight">
          Équipez votre <span className="text-accent underline decoration-accent/30">Succès</span>
        </h1>
        <p className="text-primary-text-secondary max-w-2xl mx-auto text-lg">
          Dépensez vos AutoCoins durement gagnés pour débloquer des avantages exclusifs et personnaliser votre expérience.
        </p>

        {/* Balance Card */}
        <div className="mt-10 inline-flex items-center gap-6 bg-primary-card/50 backdrop-blur-xl border border-primary-border/DEFAULT p-2 pr-8 rounded-full shadow-2xl">
          <div className="w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center shadow-lg shadow-yellow-500/20">
             <Coins className="text-black" size={24} />
          </div>
          <div className="text-left">
            <p className="text-[10px] font-black text-primary-text-secondary uppercase tracking-widest">Votre Solde Actuel</p>
            <p className="text-2xl font-black text-white">{profil?.autocoin_balance?.toLocaleString() || 0} <span className="text-yellow-500 text-sm">AC</span></p>
          </div>
        </div>
      </div>

      {/* Grid Articles */}
      <div className="max-w-7xl mx-auto">
        {message.text && (
          <div className={`mb-8 p-4 rounded-2xl flex items-center gap-3 animate-slide-up border ${
            message.type === 'success' ? 'bg-success/10 border-success/20 text-success' : 'bg-danger/10 border-danger/20 text-danger'
          }`}>
            {message.type === 'success' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
            <span className="font-bold">{message.text}</span>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {loading ? (
            Array(3).fill(0).map((_, i) => (
              <div key={i} className="h-[400px] bg-primary-card animate-pulse rounded-[2.5rem]" />
            ))
          ) : items.map(item => (
            <div key={item.id} className="group relative bg-primary-card border border-primary-border/DEFAULT rounded-[2.5rem] p-8 hover:border-accent transition-all duration-500 overflow-hidden">
              {/* Background Glow */}
              <div className="absolute -right-20 -top-20 w-64 h-64 bg-accent/5 rounded-full blur-3xl group-hover:bg-accent/10 transition-all duration-700"></div>
              
              <div className="relative z-10 h-full flex flex-col">
                <div className="w-16 h-16 bg-primary-elevated rounded-2xl flex items-center justify-center text-accent mb-8 group-hover:scale-110 transition-transform duration-500 shadow-xl border border-primary-border/DEFAULT">
                  {getIcon(item.slug)}
                </div>

                <h3 className="text-2xl font-black text-white mb-3 tracking-tight">{item.nom}</h3>
                <p className="text-primary-text-secondary text-sm leading-relaxed mb-8">
                  {item.description}
                </p>

                <div className="mt-auto">
                  <div className="flex items-center justify-between mb-6 bg-black/20 p-4 rounded-2xl border border-primary-border/DEFAULT">
                    <span className="text-xs font-bold text-primary-text-secondary uppercase">Prix</span>
                    <div className="flex items-center gap-2">
                       <span className="text-xl font-black text-white">{item.prix_ac}</span>
                       <Coins className="text-yellow-500" size={16} />
                    </div>
                  </div>

                  <button 
                    onClick={() => handleBuy(item.id, item.nom)}
                    disabled={buyingId || (profil?.autocoin_balance < item.prix_ac)}
                    className={`w-full py-4 rounded-[1.5rem] font-black text-sm uppercase tracking-widest flex items-center justify-center gap-2 transition-all shadow-xl ${
                      profil?.autocoin_balance >= item.prix_ac 
                        ? 'bg-white text-black hover:scale-[1.02] active:scale-95' 
                        : 'bg-primary-elevated text-primary-text-secondary cursor-not-allowed opacity-50'
                    }`}
                  >
                    {buyingId === item.id ? (
                      <Loader2 className="animate-spin" size={20} />
                    ) : profil?.autocoin_balance >= item.prix_ac ? (
                      <>Acheter maintenant <ArrowRight size={18} /></>
                    ) : (
                      <><Lock size={18} /> Solde insuffisant</>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Info */}
      <div className="max-w-4xl mx-auto mt-20 p-10 bg-gradient-to-br from-accent/5 to-transparent border border-accent/10 rounded-[3rem] text-center">
        <ShieldCheck className="text-accent mx-auto mb-6" size={48} />
        <h2 className="text-2xl font-bold text-white mb-4">Gagnez plus d'AutoCoins</h2>
        <p className="text-primary-text-secondary mb-8">
          Chaque estimation, alerte configurée et recherche sauvegardée vous rapporte des AC. 
          Les membres <span className="text-accent font-bold">Premium</span> gagnent des AC 2x plus vite !
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <div className="px-6 py-3 bg-primary-card rounded-2xl border border-primary-border/DEFAULT text-sm font-bold text-white flex items-center gap-2">
             <Star className="text-yellow-500" size={16} /> +10 AC / Estimation
          </div>
          <div className="px-6 py-3 bg-primary-card rounded-2xl border border-primary-border/DEFAULT text-sm font-bold text-white flex items-center gap-2">
             <Star className="text-yellow-500" size={16} /> +50 AC / Défi réussi
          </div>
        </div>
      </div>
    </div>
  );
};

export default Boutique;
