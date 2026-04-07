import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axiosClient from '../api/axiosClient';
import './DashboardPage.css';

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

const formatNumber = (value) => {
  const numberValue = Number(value || 0);
  return Number.isFinite(numberValue) ? numberValue.toLocaleString() : '0';
};

const formatCurrency = (value) => {
  const numberValue = Number(value || 0);
  if (!Number.isFinite(numberValue)) {
    return '0 EUR';
  }
  return `${Math.round(numberValue).toLocaleString()} EUR`;
};

const formatPercentage = (value) => {
  const numberValue = Number(value || 0);
  if (!Number.isFinite(numberValue)) {
    return '0.0%';
  }
  return `${numberValue >= 0 ? '+' : ''}${numberValue.toFixed(1)}%`;
};

function StatCard({ label, value, helper, tone = 'neutral' }) {
  return (
    <article className={`dash-stat-card tone-${tone}`}>
      <div className="dash-stat-label">{label}</div>
      <div className="dash-stat-value">{value}</div>
      <div className="dash-stat-helper">{helper}</div>
    </article>
  );
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, profil } = useSelector((s) => s.user);

  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [lastUpdated, setLastUpdated] = useState(null);

  const loadStats = useCallback(async () => {
    setError('');
    setLoading(true);

    try {
      const { data } = await axiosClient.get('/api/dashboard/stats/');
      setStats(data?.kpis || data || {});
      setLastUpdated(new Date());
    } catch {
      setStats({});
      setError('Impossible de charger les stats pour le moment.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadStats();
  }, [loadStats]);

  const computed = useMemo(() => {
    const totalAnnonces = Number(stats?.total_annonces ?? 0);
    const bonnesAffaires = Number(stats?.bonnes_affaires ?? 0);
    const prixMoyen = Number(stats?.prix_moyen ?? 0);
    const variationPrix = Number(stats?.variation_prix_pct ?? 0);

    const goodDealRate = totalAnnonces > 0 ? (bonnesAffaires / totalAnnonces) * 100 : 0;
    const pulseRaw = 42 + goodDealRate * 0.72 - Math.min(Math.abs(variationPrix), 18) * 0.9;
    const marketPulse = clamp(Math.round(pulseRaw), 8, 97);
    const needleAngle = -120 + marketPulse * 2.4;
    const pulseDeg = 56 + marketPulse * 2.8;

    const trendDirection = variationPrix > 0 ? 'Marche en hausse' : 'Marche en baisse';
    const trendTone = variationPrix > 0 ? 'risk' : 'good';

    return {
      totalAnnonces,
      bonnesAffaires,
      prixMoyen,
      variationPrix,
      goodDealRate,
      marketPulse,
      needleAngle,
      pulseDeg,
      trendDirection,
      trendTone,
    };
  }, [stats]);

  const insights = useMemo(() => ([
    {
      title: 'Opportunites detectees',
      text: `${formatNumber(computed.bonnesAffaires)} annonces sous-evaluees identifiees.`,
    },
    {
      title: 'Niveau de tension du marche',
      text: `${formatPercentage(computed.variationPrix)} de variation globale sur les prix.`,
    },
    {
      title: 'Qualite du scan',
      text: `${computed.goodDealRate.toFixed(1)}% des annonces semblent negociables.`,
    },
  ]), [computed.bonnesAffaires, computed.variationPrix, computed.goodDealRate]);

  const quickActions = [
    {
      title: 'Scanner les annonces',
      text: 'Filtrer les nouvelles offres et comparer rapidement.',
      path: '/annonces',
    },
    {
      title: 'Lancer une estimation',
      text: 'Obtenir un prix cible en quelques secondes.',
      path: '/estimation',
    },
    {
      title: 'Configurer des alertes',
      text: 'Recevoir les nouvelles offres qui matchent vos criteres.',
      path: '/alertes',
    },
  ];

  const cardRows = [
    {
      label: 'Total annonces',
      value: formatNumber(computed.totalAnnonces),
      helper: 'Inventaire actif du marche',
      tone: 'neutral',
    },
    {
      label: 'Bonnes affaires',
      value: formatNumber(computed.bonnesAffaires),
      helper: `${computed.goodDealRate.toFixed(1)}% du stock total`,
      tone: 'good',
    },
    {
      label: 'Prix moyen',
      value: formatCurrency(computed.prixMoyen),
      helper: 'Reference moyenne observee',
      tone: 'neutral',
    },
    {
      label: 'Variation prix',
      value: formatPercentage(computed.variationPrix),
      helper: computed.trendDirection,
      tone: computed.variationPrix > 0 ? 'risk' : 'good',
    },
  ];

  const pilotLevel = profil?.nom_niveau || 'Pilote debutant';
  const pilotProgress = clamp(Number(profil?.progression_pct ?? 0), 0, 100);
  const pilotXp = Number(profil?.xp ?? 0);

  return (
    <div className="dash-page">
      <div className="dash-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Dashboard</span>
      </div>

      <header className="dash-header">
        <h1>Cockpit Dashboard</h1>
        <p>Suivi intelligent du marche automobile, en temps reel.</p>
      </header>

      {error && (
        <div className="dash-error-banner">
          <span>{error}</span>
          <button type="button" onClick={loadStats}>Reessayer</button>
        </div>
      )}

      <section className="dash-hero-grid">
        <article className="dash-panel dash-pulse-panel">
          <div className="dash-panel-head">
            <div>
              <h2>Market Pulse</h2>
              <p>Signal combine: volume, tension et opportunites.</p>
            </div>
            <button type="button" onClick={loadStats} disabled={loading}>Actualiser</button>
          </div>

          <div
            className="dash-gauge"
            style={{ '--pulse-deg': `${computed.pulseDeg}deg`, '--needle-angle': `${computed.needleAngle}deg` }}
          >
            <div className="dash-gauge-ring" />
            <div className="dash-gauge-needle-wrap">
              <span className="dash-gauge-needle" />
            </div>
            <div className="dash-gauge-core">
              <strong>{computed.marketPulse}</strong>
              <small>/ 100</small>
            </div>
          </div>

          <div className="dash-pulse-meta">
            <div>
              <span>Etat</span>
              <strong className={computed.trendTone === 'risk' ? 'tone-risk' : 'tone-good'}>
                {computed.trendDirection}
              </strong>
            </div>
            <div>
              <span>Derniere sync</span>
              <strong>{lastUpdated ? lastUpdated.toLocaleTimeString() : '--:--:--'}</strong>
            </div>
          </div>
        </article>

        <article className="dash-panel dash-pilot-panel">
          <div className="dash-pilot-head">
            <div className="dash-pilot-avatar">{user?.username?.[0]?.toUpperCase() || 'U'}</div>
            <div>
              <h2>{user?.username || 'Utilisateur'}</h2>
              <p>{pilotLevel}</p>
            </div>
          </div>

          <div className="dash-pilot-xp">
            <div className="dash-pilot-xp-line">
              <span>XP actuel</span>
              <strong>{formatNumber(pilotXp)} XP</strong>
            </div>
            <div className="dash-pilot-progress">
              <div style={{ width: `${pilotProgress}%` }} />
            </div>
            <div className="dash-pilot-xp-foot">
              <span>Niveau {profil?.niveau || 1}</span>
              <span>{pilotProgress.toFixed(0)}% complet</span>
            </div>
          </div>

          <div className="dash-pilot-actions">
            <button type="button" onClick={() => navigate('/profil')}>Mon profil</button>
            <button type="button" onClick={() => navigate('/abonnement')}>Mon abonnement</button>
          </div>
        </article>
      </section>

      <section className="dash-stats-grid">
        {loading
          ? Array.from({ length: 4 }).map((_, idx) => (
            <article key={idx} className="dash-stat-card dash-loading-card" />
          ))
          : cardRows.map((card) => (
            <StatCard
              key={card.label}
              label={card.label}
              value={card.value}
              helper={card.helper}
              tone={card.tone}
            />
          ))}
      </section>

      <section className="dash-bottom-grid">
        <article className="dash-panel">
          <div className="dash-subhead">
            <h3>Insights du jour</h3>
            <p>Lecture rapide des signaux importants.</p>
          </div>
          <div className="dash-insights-list">
            {insights.map((item) => (
              <div key={item.title} className="dash-insight-item">
                <h4>{item.title}</h4>
                <p>{item.text}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="dash-panel">
          <div className="dash-subhead">
            <h3>Actions rapides</h3>
            <p>Acces direct aux modules cles.</p>
          </div>
          <div className="dash-action-list">
            {quickActions.map((action) => (
              <button key={action.path} type="button" onClick={() => navigate(action.path)}>
                <div>
                  <strong>{action.title}</strong>
                  <span>{action.text}</span>
                </div>
                <em>Ouvrir</em>
              </button>
            ))}
          </div>
        </article>
      </section>
    </div>
  );
}
