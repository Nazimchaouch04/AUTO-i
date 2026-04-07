import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';

export default function AbonnementPage() {
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [current, setCurrent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const plansRes = await axiosClient.get('/api/subscriptions/plans/');
        setPlans(plansRes.data?.results || plansRes.data || []);
      } catch (err) {
        setPlans([]);
      }

      try {
        const currentRes = await axiosClient.get('/api/subscriptions/mon-abonnement/');
        setCurrent(currentRes.data || null);
      } catch (err) {
        setCurrent(null);
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
        <span style={{ color: '#8B8BA0' }}>Abonnement</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>
        Abonnement
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Gérer mon plan et mes options.
      </p>

      {loading ? (
        <p style={{ color: '#8B8BA0' }}>Chargement des plans...</p>
      ) : (
        <>
          <div style={{ marginBottom: 14, color: '#8B8BA0', fontSize: 13 }}>
            Plan actuel: <b style={{ color: '#F0F0F5' }}>{current?.plan || 'Free'}</b>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 10 }}>
            {plans.map((p) => (
              <div
                key={p.id}
                style={{
                  background: '#13131E',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: 10,
                  padding: 12,
                }}
              >
                <div style={{ fontWeight: 700, color: '#F0F0F5' }}>{p.nom}</div>
                <div style={{ color: '#6C63FF', fontSize: 22, fontWeight: 700, marginTop: 8 }}>
                  {Number(p.prix_mensuel || 0).toLocaleString()} €
                </div>
                <div style={{ color: '#8B8BA0', fontSize: 12, marginTop: 6 }}>
                  {p.estimations_par_mois} estimations/mois • {p.alertes_max} alertes
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
