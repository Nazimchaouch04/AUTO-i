import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';

export default function BattlesPage() {
  const navigate = useNavigate();
  const [battles, setBattles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/annonces/battles/');
        setBattles(data?.results || data || []);
      } catch (err) {
        setBattles([]);
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
        <span style={{ color: '#8B8BA0' }}>Battles 1v1</span>
      </div>
      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>Battles 1v1</h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>Affronte d’autres joueurs.</p>
      {loading && <p style={{ color: '#8B8BA0' }}>Chargement...</p>}
      {!loading && battles.length === 0 && <p style={{ color: '#8B8BA0' }}>Aucune battle active.</p>}
      {!loading && battles.length > 0 && (
        <div style={{ display: 'grid', gap: 8 }}>
          {battles.map((b) => (
            <div key={b.id} style={{ background: '#13131E', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, padding: 10 }}>
              <div style={{ fontWeight: 600 }}>
                {b.vehicule_1_details?.vehicule_marque} vs {b.vehicule_2_details?.vehicule_marque}
              </div>
              <div style={{ color: '#8B8BA0', fontSize: 12, marginTop: 4 }}>
                Votes: {b.votes_v1 ?? 0} - {b.votes_v2 ?? 0}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
