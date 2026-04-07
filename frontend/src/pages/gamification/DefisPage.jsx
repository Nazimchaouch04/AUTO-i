import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';

export default function DefisPage() {
  const navigate = useNavigate();
  const [defis, setDefis] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/gamification/defis/');
        setDefis(data?.results || data || []);
      } catch (err) {
        setDefis([]);
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
        <span style={{ color: '#8B8BA0' }}>Défis</span>
      </div>
      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>Défis</h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>Complète tes objectifs.</p>
      {loading && <p style={{ color: '#8B8BA0' }}>Chargement...</p>}
      {!loading && defis.length === 0 && <p style={{ color: '#8B8BA0' }}>Aucun défi actif.</p>}
      {!loading && defis.length > 0 && (
        <div style={{ display: 'grid', gap: 8 }}>
          {defis.map((d) => (
            <div key={d.id} style={{ background: '#13131E', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, padding: 10 }}>
              <div style={{ fontWeight: 600 }}>{d.titre}</div>
              <div style={{ color: '#8B8BA0', fontSize: 12, marginTop: 3 }}>{d.description}</div>
              <div style={{ color: '#6C63FF', fontSize: 12, marginTop: 6 }}>
                Récompense: {d.xp_reward ?? 0} XP • {d.ac_reward ?? 0} AC
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
