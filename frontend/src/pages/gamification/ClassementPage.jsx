import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';

export default function ClassementPage() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/gamification/leaderboard/');
        setRows(data?.results || data || []);
      } catch (err) {
        setRows([]);
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
        <span style={{ color: '#8B8BA0' }}>Classement</span>
      </div>
      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>Classement</h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>Top joueurs AutoIntel.</p>
      {loading && <p style={{ color: '#8B8BA0' }}>Chargement...</p>}
      {!loading && rows.length === 0 && <p style={{ color: '#8B8BA0' }}>Aucune donnée de classement.</p>}
      {!loading && rows.length > 0 && (
        <div style={{ display: 'grid', gap: 8 }}>
          {rows.slice(0, 20).map((u, idx) => (
            <div
              key={`${u.id}-${idx}`}
              style={{
                background: '#13131E',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 10,
                padding: 10,
                display: 'flex',
                justifyContent: 'space-between',
              }}
            >
              <div>{idx + 1}. {u.username || 'Utilisateur'}</div>
              <div style={{ color: '#6C63FF', fontWeight: 700 }}>{u.xp ?? 0} XP</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
