import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import './AppPages.css';

const formatCurrency = (value) => `${Math.round(Number(value || 0)).toLocaleString()} EUR`;
const formatKm = (value) => `${Math.round(Number(value || 0)).toLocaleString()} km`;

export default function AnnoncesPage() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/annonces/?page=1');
        setItems(data?.results || data || []);
      } catch {
        setItems([]);
        setError('Impossible de charger les annonces.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const stats = useMemo(() => {
    const total = items.length;
    const avgPrice = total > 0
      ? items.reduce((sum, a) => sum + Number(a.prix || 0), 0) / total
      : 0;
    const avgKm = total > 0
      ? items.reduce((sum, a) => sum + Number(a.kilometrage || 0), 0) / total
      : 0;

    const brands = {};
    items.forEach((a) => {
      const key = (a.vehicule_marque || 'N/A').toUpperCase();
      brands[key] = (brands[key] || 0) + 1;
    });

    const topBrand = Object.entries(brands).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];

    return { total, avgPrice, avgKm, topBrand };
  }, [items]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Annonces</span>
      </div>

      <div className="app-header">
        <h1>Annonces Market</h1>
        <p>Liste dynamique des vehicules avec signaux rapides d'opportunite.</p>
      </div>

      <div className="app-grid-half" style={{ marginBottom: 12 }}>
        <div className="app-kpi accent">
          <label>Annonces chargees</label>
          <strong>{stats.total.toLocaleString()}</strong>
          <small>Page de surveillance active</small>
        </div>
        <div className="app-kpi">
          <label>Prix moyen</label>
          <strong>{formatCurrency(stats.avgPrice)}</strong>
          <small>Estimation moyenne des annonces visibles</small>
        </div>
        <div className="app-kpi">
          <label>Kilometrage moyen</label>
          <strong>{formatKm(stats.avgKm)}</strong>
          <small>Etat d'usure moyen du stock</small>
        </div>
        <div className="app-kpi good">
          <label>Marque dominante</label>
          <strong>{stats.topBrand[0]}</strong>
          <small>{stats.topBrand[1]} annonces</small>
        </div>
      </div>

      {loading && <div className="app-loading">Chargement des annonces...</div>}
      {!loading && error && <div className="app-error">{error}</div>}
      {!loading && !error && items.length === 0 && (
        <div className="app-empty">Aucune annonce disponible pour le moment.</div>
      )}

      {!loading && !error && items.length > 0 && (
        <div className="app-stack">
          {items.slice(0, 18).map((a) => (
            <article key={a.id} className="app-list-item">
              <div>
                <div className="app-list-title">
                  {(a.vehicule_marque || 'N/A')} {(a.vehicule_modele || '')} {a.annee || ''}
                </div>
                <div className="app-list-meta">
                  {formatKm(a.kilometrage)} - {(a.carburant || 'N/A').toUpperCase()} - {a.ville || 'Ville inconnue'}
                </div>
                <div className="app-chip-row" style={{ marginTop: 8 }}>
                  <span className="app-badge">{a.boite || 'boite N/A'}</span>
                  <span className="app-badge">{a.pays || 'pays N/A'}</span>
                  <span className="app-badge">{a.source || 'source auto'}</span>
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <div className="app-price">{formatCurrency(a.prix)}</div>
                <button
                  type="button"
                  className="app-btn-ghost"
                  style={{ marginTop: 8 }}
                  onClick={() => navigate('/estimation')}
                >
                  Estimer similaire
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
