import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import './AppPages.css';

export default function AlertesPage() {
  const navigate = useNavigate();
  const [alertes, setAlertes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/alertes/');
        setAlertes(data?.results || data || []);
      } catch {
        setError('Impossible de charger les alertes.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const stats = useMemo(() => {
    const total = alertes.length;
    const active = alertes.filter((a) => a.active !== false && a.is_active !== false).length;
    const premium = alertes.filter((a) => Number(a.priorite || 0) >= 2).length;
    return { total, active, premium };
  }, [alertes]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Alertes</span>
      </div>

      <div className="app-header">
        <h1>Centre Alertes</h1>
        <p>Surveillez le marche automatiquement et reagissez au bon moment.</p>
      </div>

      <div className="app-grid-three" style={{ marginBottom: 12 }}>
        <div className="app-kpi accent">
          <label>Total alertes</label>
          <strong>{stats.total}</strong>
          <small>Regles configurees</small>
        </div>
        <div className="app-kpi good">
          <label>Alertes actives</label>
          <strong>{stats.active}</strong>
          <small>Suivi temps reel en cours</small>
        </div>
        <div className="app-kpi warn">
          <label>Alertes prioritaires</label>
          <strong>{stats.premium}</strong>
          <small>Opportunites a verifier vite</small>
        </div>
      </div>

      {loading && <div className="app-loading">Chargement des alertes...</div>}
      {!loading && error && <div className="app-error">{error}</div>}
      {!loading && !error && alertes.length === 0 && (
        <div className="app-empty">Aucune alerte active. Creez votre premier suivi.</div>
      )}

      {!loading && !error && alertes.length > 0 && (
        <div className="app-stack" style={{ marginBottom: 12 }}>
          {alertes.map((a) => {
            const active = a.active !== false && a.is_active !== false;
            return (
              <article key={a.id} className="app-list-item">
                <div>
                  <div className="app-list-title">{a.titre || `${a.marque || 'Marque'} ${a.modele || ''}`.trim()}</div>
                  <div className="app-list-meta">
                    {(a.marque || 'Toutes marques')} {(a.modele || '')} - Prix max {a.prix_max ? `${Number(a.prix_max).toLocaleString()} EUR` : 'sans limite'}
                  </div>
                  <div className="app-chip-row" style={{ marginTop: 8 }}>
                    <span className="app-badge">Frequence: {a.frequence || 'quotidienne'}</span>
                    <span className="app-badge">Canal: {a.canal || 'app'}</span>
                  </div>
                </div>

                <div>
                  <span className={`app-badge ${active ? 'app-pill-good' : 'app-pill-danger'}`}>
                    {active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </article>
            );
          })}
        </div>
      )}

      <div className="app-grid-half">
        <button className="app-btn-ghost" type="button" onClick={() => navigate('/annonces')}>
          Scanner nouvelles annonces
        </button>
        <button className="app-btn-ghost" type="button" onClick={() => navigate('/estimation')}>
          Lancer estimation rapide
        </button>
      </div>
    </div>
  );
}
