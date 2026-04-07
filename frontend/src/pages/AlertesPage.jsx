import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';

export default function AlertesPage() {
  const navigate = useNavigate();
  const [alertes, setAlertes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/alertes/');
        setAlertes(data?.results || data || []);
      } catch (err) {
        setError('Impossible de charger les alertes.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

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
        <span style={{ color: '#8B8BA0' }}>Alertes</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>
        Mes alertes
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Suivi automatique du marché.
      </p>

      {loading && <p style={{ color: '#8B8BA0', fontSize: 14 }}>Chargement des alertes...</p>}
      {!loading && error && <p style={{ color: '#FCA5A5', fontSize: 14 }}>{error}</p>}
      {!loading && !error && alertes.length === 0 && (
        <p style={{ color: '#8B8BA0', fontSize: 14 }}>Aucune alerte active.</p>
      )}

      {!loading && !error && alertes.length > 0 && (
        <div style={{ display: 'grid', gap: 10 }}>
          {alertes.map((a) => (
            <div
              key={a.id}
              style={{
                background: '#13131E',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 10,
                padding: 12,
              }}
            >
              <div style={{ color: '#F0F0F5', fontSize: 14, fontWeight: 600 }}>
                {a.titre}
              </div>
              <div style={{ color: '#8B8BA0', fontSize: 12, marginTop: 4 }}>
                {a.marque || 'Toutes marques'} {a.modele || ''} • Max {a.prix_max || '∞'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
