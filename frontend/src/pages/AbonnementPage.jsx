import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import './AppPages.css';

const formatCurrency = (value) => `${Math.round(Number(value || 0)).toLocaleString()} EUR`;

export default function AbonnementPage() {
  const navigate = useNavigate();

  const [plans, setPlans] = useState([]);
  const [current, setCurrent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);

      try {
        const plansRes = await axiosClient.get('/api/subscriptions/plans/');
        setPlans(plansRes.data?.results || plansRes.data || []);
      } catch {
        setPlans([]);
      }

      try {
        const currentRes = await axiosClient.get('/api/subscriptions/mon-abonnement/');
        setCurrent(currentRes.data || null);
      } catch {
        setCurrent(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const currentPlanName = useMemo(() => (
    current?.plan_details?.nom || current?.plan || current?.nom || 'Free'
  ), [current]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Abonnement</span>
      </div>

      <div className="app-header">
        <h1>Abonnement</h1>
        <p>Choisissez la puissance qui correspond a votre rythme d'analyse.</p>
      </div>

      {loading && <div className="app-loading">Chargement des plans...</div>}
      {!loading && error && <div className="app-error">{error}</div>}

      {!loading && (
        <>
          <article className="app-card" style={{ marginBottom: 12 }}>
            <h3>Plan actuel</h3>
            <p className="app-card-sub">Actif maintenant: <span className="app-pill-good">{currentPlanName}</span></p>
            <div className="app-grid-half" style={{ marginTop: 10 }}>
              <div className="app-kpi">
                <label>Estimations utilisees</label>
                <strong>{Number(current?.estimations_utilisees ?? 0).toLocaleString()}</strong>
                <small>Mois en cours</small>
              </div>
              <div className="app-kpi">
                <label>Alertes actives</label>
                <strong>{Number(current?.alertes_actives ?? 0).toLocaleString()}</strong>
                <small>Surveillance en direct</small>
              </div>
            </div>
          </article>

          {plans.length === 0 ? (
            <div className="app-empty">Aucun plan recu depuis l'API.</div>
          ) : (
            <div className="app-grid-cards">
              {plans.map((p) => {
                const isCurrent = String(p.nom || '').toLowerCase() === String(currentPlanName || '').toLowerCase();
                return (
                  <article key={p.id} className="app-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 8 }}>
                      <h3>{p.nom}</h3>
                      {isCurrent && <span className="app-badge app-pill-good">Actuel</span>}
                    </div>

                    <div style={{ marginTop: 10 }}>
                      <div className="app-price">{formatCurrency(p.prix_mensuel)}</div>
                      <div className="app-card-sub">/ mois</div>
                    </div>

                    <div className="app-stack" style={{ marginTop: 12 }}>
                      <div className="app-list-meta">{Number(p.estimations_par_mois ?? 0).toLocaleString()} estimations / mois</div>
                      <div className="app-list-meta">{Number(p.alertes_max ?? 0).toLocaleString()} alertes max</div>
                      <div className="app-list-meta">Support: {p.support || 'standard'}</div>
                    </div>

                    <button className="app-btn" type="button" style={{ marginTop: 12 }}>
                      {isCurrent ? 'Plan actif' : 'Choisir ce plan'}
                    </button>
                  </article>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
