import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';

export default function BoutiquePage() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/gamification/shop/');
        setItems(data?.results || data || []);
      } catch (err) {
        setItems([]);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div style={{ color: '#F0F0F5', padding: '0 0 32px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 24, fontSize: 13 }}>
        <span onClick={() => navigate('/dashboard')} style={{ color: '#6C63FF', cursor: 'pointer' }}>Accueil</span>
        <span style={{ color: '#8B8BA0' }}>›</span>
        <span style={{ color: '#8B8BA0' }}>Boutique</span>
      </div>
      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>Boutique</h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>Dépense tes AutoCoins.</p>
      {loading && <p style={{ color: '#8B8BA0' }}>Chargement...</p>}
      {!loading && items.length === 0 && <p style={{ color: '#8B8BA0' }}>Boutique vide ou inaccessible.</p>}
      {!loading && items.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 10 }}>
          {items.map((i) => (
            <div
              key={i.id}
              style={{ background: '#13131E', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, padding: 12 }}
            >
              <div style={{ fontWeight: 700 }}>{i.nom}</div>
              <div style={{ color: '#8B8BA0', fontSize: 12, marginTop: 5 }}>{i.description}</div>
              <div style={{ color: '#F59E0B', fontWeight: 700, marginTop: 8 }}>{i.prix_ac ?? 0} AC</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
