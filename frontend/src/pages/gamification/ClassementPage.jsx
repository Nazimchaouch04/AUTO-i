import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';
import '../AppPages.css';

export default function ClassementPage() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/gamification/leaderboard/');
        setRows(data?.results || data || []);
      } catch {
        setRows([]);
        setError('Impossible de charger le classement.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const podium = useMemo(() => rows.slice(0, 3), [rows]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Classement</span>
      </div>

      <div className="app-header">
        <h1>Classement Joueurs</h1>
        <p>Top performers AutoIntel par XP et activite.</p>
      </div>

      {loading && <div className="app-loading">Chargement du classement...</div>}
      {!loading && error && <div className="app-error">{error}</div>}

      {!loading && !error && rows.length === 0 && (
        <div className="app-empty">Aucune donnee de classement disponible.</div>
      )}

      {!loading && !error && rows.length > 0 && (
        <>
          <div className="app-grid-three" style={{ marginBottom: 12 }}>
            {podium.map((u, idx) => (
              <article key={`podium-${u.id || idx}`} className="app-kpi accent">
                <label>Top {idx + 1}</label>
                <strong>{u.username || 'Utilisateur'}</strong>
                <small>{Number(u.xp ?? 0).toLocaleString()} XP</small>
              </article>
            ))}
          </div>

          <article className="app-card">
            <h3>Top 20</h3>
            <table className="app-table" style={{ marginTop: 10 }}>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Joueur</th>
                  <th>XP</th>
                  <th>Niveau</th>
                </tr>
              </thead>
              <tbody>
                {rows.slice(0, 20).map((u, idx) => (
                  <tr key={`${u.id}-${idx}`}>
                    <td>{idx + 1}</td>
                    <td>{u.username || 'Utilisateur'}</td>
                    <td>{Number(u.xp ?? 0).toLocaleString()}</td>
                    <td>{u.niveau ?? 1}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </article>
        </>
      )}
    </div>
  );
}
