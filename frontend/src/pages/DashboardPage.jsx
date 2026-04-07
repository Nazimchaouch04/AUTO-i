import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/dashboard/stats/');
        setStats(data?.kpis || null);
      } catch (err) {
        setStats(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const cards = [
    { label: 'Total annonces', value: stats?.total_annonces ?? 0 },
    { label: 'Bonnes affaires', value: stats?.bonnes_affaires ?? 0 },
    { label: 'Prix moyen', value: stats?.prix_moyen ?? 0 },
    { label: 'Variation prix %', value: stats?.variation_prix_pct ?? 0 },
  ];

  return (
    <div style={{ color: '#F0F0F5', padding: '0 0 32px' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 6,
          marginBottom: 24,
          fontSize: 13,
        }}
      >
        <span onClick={() => navigate('/dashboard')} style={{ color: '#6C63FF', cursor: 'pointer' }}>
          Accueil
        </span>
        <span style={{ color: '#8B8BA0' }}>›</span>
        <span style={{ color: '#8B8BA0' }}>Dashboard</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>
        Dashboard
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Vue d’ensemble du marché AutoIntel.
      </p>

      {loading ? (
        <p style={{ color: '#8B8BA0', fontSize: 14 }}>Chargement des statistiques...</p>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: 12,
          }}
        >
          {cards.map((c) => (
            <div
              key={c.label}
              style={{
                background: '#13131E',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 10,
                padding: 14,
              }}
            >
              <div style={{ color: '#8B8BA0', fontSize: 12 }}>{c.label}</div>
              <div style={{ color: '#F0F0F5', fontSize: 24, fontWeight: 700, marginTop: 6 }}>
                {typeof c.value === 'number' ? c.value.toLocaleString() : c.value}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
