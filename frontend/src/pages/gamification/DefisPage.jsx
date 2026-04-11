import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';
import '../AppPages.css';

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

export default function DefisPage() {
  const navigate = useNavigate();
  const [defis, setDefis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/gamification/defis/');
        setDefis(data?.results || data || []);
      } catch {
        setDefis([]);
        setError('Impossible de charger les defis.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const totals = useMemo(() => {
    const total = defis.length;
    const completed = defis.filter((d) => d.termine === true || d.completed === true).length;
    const totalXp = defis.reduce((sum, d) => sum + Number(d.xp_reward || 0), 0);
    return { total, completed, totalXp };
  }, [defis]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Defis</span>
      </div>

      <div className="app-header">
        <h1>Defis Actifs</h1>
        <p>Objectifs quotidiens et hebdomadaires pour accelerer votre progression.</p>
      </div>

      <div className="app-grid-three" style={{ marginBottom: 12 }}>
        <div className="app-kpi accent">
          <label>Total defis</label>
          <strong>{totals.total}</strong>
          <small>Disponibles actuellement</small>
        </div>
        <div className="app-kpi good">
          <label>Completes</label>
          <strong>{totals.completed}</strong>
          <small>Objectifs valides</small>
        </div>
        <div className="app-kpi warn">
          <label>XP potentiel</label>
          <strong>{totals.totalXp.toLocaleString()}</strong>
          <small>Recompense totale possible</small>
        </div>
      </div>

      {loading && <div className="app-loading">Chargement des defis...</div>}
      {!loading && error && <div className="app-error">{error}</div>}
      {!loading && !error && defis.length === 0 && <div className="app-empty">Aucun defi actif pour le moment.</div>}

      {!loading && !error && defis.length > 0 && (
        <div className="app-grid-cards">
          {defis.map((d) => {
            const progress = clamp(Number(d.progression_pct ?? d.progress ?? 0), 0, 100);
            const done = d.termine === true || d.completed === true || progress >= 100;

            return (
              <article key={d.id} className="app-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
                  <h3>{d.titre || 'Defi sans titre'}</h3>
                  <span className={`app-badge ${done ? 'app-pill-good' : 'app-pill-warn'}`}>
                    {done ? 'Complete' : 'En cours'}
                  </span>
                </div>

                <p className="app-card-sub" style={{ marginTop: 8 }}>{d.description || 'Aucune description.'}</p>

                <div className="app-progress" style={{ marginTop: 10 }}>
                  <div style={{ width: `${progress}%` }} />
                </div>

                <div className="app-list-meta" style={{ marginTop: 8 }}>
                  Progression: {progress.toFixed(0)}%
                </div>

                <div className="app-chip-row" style={{ marginTop: 10 }}>
                  <span className="app-badge">{Number(d.xp_reward || 0).toLocaleString()} XP</span>
                  <span className="app-badge">{Number(d.ac_reward || 0).toLocaleString()} AC</span>
                  <span className="app-badge">{d.type || 'defi'}</span>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}
