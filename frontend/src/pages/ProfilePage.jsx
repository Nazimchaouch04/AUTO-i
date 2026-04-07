import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import { useDispatch } from 'react-redux';
import { updateProfil } from '../store/userSlice';
import './AppPages.css';

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

export default function ProfilePage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      setError('');
      setLoading(true);
      try {
        const { data } = await axiosClient.get('/api/auth/profile/');
        setProfile(data || null);
        if (data?.profil) {
          dispatch(updateProfil(data.profil));
        }
      } catch {
        setError('Impossible de charger le profil.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [dispatch]);

  const stats = useMemo(() => {
    const xp = Number(profile?.profil?.xp ?? 0);
    const niveau = Number(profile?.profil?.niveau ?? 1);
    const progress = clamp(Number(profile?.profil?.progression_pct ?? 0), 0, 100);
    const autoCoins = Number(profile?.profil?.autocoin_balance ?? 0);
    const alertes = Number(profile?.profil?.alertes_actives ?? 0);
    return { xp, niveau, progress, autoCoins, alertes };
  }, [profile]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Mon profil</span>
      </div>

      <div className="app-header">
        <h1>Mon Profil</h1>
        <p>Pilotez votre progression et vos donnees de compte AutoIntel.</p>
      </div>

      {loading && <div className="app-loading">Chargement du profil...</div>}
      {!loading && error && <div className="app-error">{error}</div>}

      {!loading && !error && (
        <>
          <div className="app-grid-two" style={{ marginBottom: 12 }}>
            <article className="app-card">
              <h3>Identite compte</h3>
              <div className="app-stack" style={{ marginTop: 10 }}>
                <div className="app-list-item">
                  <div>
                    <div className="app-list-title">Nom utilisateur</div>
                    <div className="app-list-meta">{profile?.user?.username || 'N/A'}</div>
                  </div>
                  <span className="app-badge">Compte actif</span>
                </div>
                <div className="app-list-item">
                  <div>
                    <div className="app-list-title">Email</div>
                    <div className="app-list-meta">{profile?.user?.email || 'N/A'}</div>
                  </div>
                  <span className="app-badge">Verifie</span>
                </div>
              </div>
            </article>

            <article className="app-card">
              <h3>Progression joueur</h3>
              <p className="app-card-sub">Niveau {stats.niveau} - {stats.xp.toLocaleString()} XP</p>
              <div className="app-progress" style={{ marginTop: 10 }}>
                <div style={{ width: `${stats.progress}%` }} />
              </div>
              <div className="app-list-meta" style={{ marginTop: 8 }}>{stats.progress.toFixed(0)}% vers le prochain niveau</div>

              <div className="app-grid-half" style={{ marginTop: 12 }}>
                <div className="app-kpi good">
                  <label>AutoCoins</label>
                  <strong>{stats.autoCoins.toLocaleString()}</strong>
                  <small>Monnaie interne</small>
                </div>
                <div className="app-kpi accent">
                  <label>Alertes actives</label>
                  <strong>{stats.alertes}</strong>
                  <small>Surveillance en cours</small>
                </div>
              </div>
            </article>
          </div>

          <div className="app-grid-half">
            <button className="app-btn-ghost" type="button" onClick={() => navigate('/abonnement')}>
              Gerer abonnement
            </button>
            <button className="app-btn-ghost" type="button" onClick={() => navigate('/classement')}>
              Voir classement
            </button>
          </div>
        </>
      )}
    </div>
  );
}
