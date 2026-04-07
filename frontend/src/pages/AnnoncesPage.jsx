import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';

export default function AnnoncesPage() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/annonces/?page=1');
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
        <span style={{ color: '#8B8BA0' }}>Annonces</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>
        Annonces
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Liste des annonces automobiles récentes.
      </p>

      {loading ? (
        <p style={{ color: '#8B8BA0', fontSize: 14 }}>Chargement des annonces...</p>
      ) : items.length === 0 ? (
        <p style={{ color: '#8B8BA0', fontSize: 14 }}>Aucune annonce disponible.</p>
      ) : (
        <div style={{ display: 'grid', gap: 10 }}>
          {items.slice(0, 12).map((a) => (
            <div
              key={a.id}
              style={{
                background: '#13131E',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 10,
                padding: 12,
                display: 'flex',
                justifyContent: 'space-between',
                gap: 16,
              }}
            >
              <div>
                <div style={{ fontSize: 14, color: '#F0F0F5', fontWeight: 600 }}>
                  {a.vehicule_marque} {a.vehicule_modele} {a.annee}
                </div>
                <div style={{ fontSize: 12, color: '#8B8BA0', marginTop: 4 }}>
                  {a.kilometrage?.toLocaleString()} km • {a.carburant} • {a.ville || 'N/A'}
                </div>
              </div>
              <div style={{ color: '#6C63FF', fontWeight: 700 }}>
                {typeof a.prix === 'number' ? a.prix.toLocaleString() : a.prix} €
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
