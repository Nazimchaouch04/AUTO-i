import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axiosClient from '../../api/axiosClient';
import '../AppPages.css';

export default function BoutiquePage() {
  const navigate = useNavigate();
  const { profil } = useSelector((s) => s.user);

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/gamification/shop/');
        setItems(data?.results || data || []);
      } catch {
        setItems([]);
        setError('Impossible de charger la boutique.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const wallet = Number(profil?.autocoin_balance ?? 0);

  const affordability = useMemo(() => {
    const affordable = items.filter((i) => Number(i.prix_ac || 0) <= wallet).length;
    return { affordable, total: items.length };
  }, [items, wallet]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Boutique</span>
      </div>

      <div className="app-header">
        <h1>Boutique AutoCoins</h1>
        <p>Depensez vos AC pour debloquer des avantages de progression.</p>
      </div>

      <div className="app-grid-half" style={{ marginBottom: 12 }}>
        <div className="app-kpi warn">
          <label>Mon solde</label>
          <strong>{wallet.toLocaleString()} AC</strong>
          <small>AutoCoins disponibles</small>
        </div>
        <div className="app-kpi accent">
          <label>Objets accessibles</label>
          <strong>{affordability.affordable}/{affordability.total}</strong>
          <small>Selon votre solde actuel</small>
        </div>
      </div>

      {loading && <div className="app-loading">Chargement de la boutique...</div>}
      {!loading && error && <div className="app-error">{error}</div>}
      {!loading && !error && items.length === 0 && <div className="app-empty">Boutique vide pour le moment.</div>}

      {!loading && !error && items.length > 0 && (
        <div className="app-grid-cards">
          {items.map((i) => {
            const price = Number(i.prix_ac || 0);
            const canBuy = price <= wallet;

            return (
              <article key={i.id} className="app-card">
                <h3>{i.nom || 'Item'}</h3>
                <p className="app-card-sub">{i.description || 'Objet boutique.'}</p>

                <div className="app-chip-row" style={{ marginTop: 10 }}>
                  <span className="app-badge">{price.toLocaleString()} AC</span>
                  <span className={`app-badge ${canBuy ? 'app-pill-good' : 'app-pill-danger'}`}>
                    {canBuy ? 'Achat possible' : 'Solde insuffisant'}
                  </span>
                </div>

                <button className="app-btn" type="button" style={{ marginTop: 12 }}>
                  {canBuy ? 'Acheter' : 'Gagner plus de AC'}
                </button>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}
