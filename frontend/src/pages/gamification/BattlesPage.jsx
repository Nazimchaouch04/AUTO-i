import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';
import '../AppPages.css';

const pct = (a, b) => {
  const total = Number(a || 0) + Number(b || 0);
  if (!total) return 50;
  return Math.round((Number(a || 0) / total) * 100);
};

export default function BattlesPage() {
  const navigate = useNavigate();
  const [battles, setBattles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/annonces/battles/');
        setBattles(data?.results || data || []);
      } catch {
        setBattles([]);
        setError('Impossible de charger les battles.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Battles 1v1</span>
      </div>

      <div className="app-header">
        <h1>Battles 1v1</h1>
        <p>Comparez deux vehicules et suivez les votes de la communaute.</p>
      </div>

      {loading && <div className="app-loading">Chargement des battles...</div>}
      {!loading && error && <div className="app-error">{error}</div>}
      {!loading && !error && battles.length === 0 && <div className="app-empty">Aucune battle active.</div>}

      {!loading && !error && battles.length > 0 && (
        <div className="app-stack">
          {battles.map((b) => {
            const v1 = Number(b.votes_v1 ?? 0);
            const v2 = Number(b.votes_v2 ?? 0);
            const p1 = pct(v1, v2);
            const p2 = 100 - p1;

            const car1 = `${b.vehicule_1_details?.vehicule_marque || 'Vehicule A'} ${b.vehicule_1_details?.vehicule_modele || ''}`.trim();
            const car2 = `${b.vehicule_2_details?.vehicule_marque || 'Vehicule B'} ${b.vehicule_2_details?.vehicule_modele || ''}`.trim();

            return (
              <article key={b.id} className="app-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, marginBottom: 8 }}>
                  <h3>{car1}</h3>
                  <span className="app-badge">VS</span>
                  <h3>{car2}</h3>
                </div>

                <div className="app-progress" style={{ height: 10 }}>
                  <div style={{ width: `${p1}%`, background: 'linear-gradient(90deg,#6c63ff,#22d3ee)' }} />
                </div>

                <div className="app-grid-half" style={{ marginTop: 8 }}>
                  <div className="app-list-meta">{car1}: {v1} votes ({p1}%)</div>
                  <div className="app-list-meta" style={{ textAlign: 'right' }}>{car2}: {v2} votes ({p2}%)</div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}
