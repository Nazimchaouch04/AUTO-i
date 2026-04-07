import { useNavigate } from 'react-router-dom';
import '../AppPages.css';

const rewards = [
  { level: 5, label: 'Booster XP x2', premium: false },
  { level: 10, label: 'Pack cards Rare', premium: true },
  { level: 15, label: '500 AutoCoins', premium: false },
  { level: 20, label: 'Badge Velocity', premium: true },
  { level: 25, label: 'Skin Dashboard Neon', premium: true },
];

export default function SeasonPassPage() {
  const navigate = useNavigate();

  const currentLevel = 12;
  const progress = 47;

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Season Pass</span>
      </div>

      <div className="app-header">
        <h1>Season Pass</h1>
        <p>Racing Edition Saison 1 - progression et recompenses exclusives.</p>
      </div>

      <article className="app-card" style={{ marginBottom: 12 }}>
        <h3>Niveau actuel: {currentLevel}</h3>
        <p className="app-card-sub">Progression globale de la saison en cours.</p>
        <div className="app-progress" style={{ marginTop: 10 }}>
          <div style={{ width: `${progress}%` }} />
        </div>
        <div className="app-list-meta" style={{ marginTop: 8 }}>{progress}% vers le niveau {currentLevel + 1}</div>
      </article>

      <div className="app-stack">
        {rewards.map((r) => (
          <article key={r.level} className="app-list-item">
            <div>
              <div className="app-list-title">Niveau {r.level}</div>
              <div className="app-list-meta">{r.label}</div>
            </div>
            <div className="app-chip-row">
              <span className={`app-badge ${r.premium ? 'app-pill-warn' : 'app-pill-good'}`}>
                {r.premium ? 'Premium' : 'Gratuit'}
              </span>
            </div>
          </article>
        ))}
      </div>

      <button className="app-btn" type="button" style={{ marginTop: 12 }} onClick={() => navigate('/abonnement')}>
        Passer au pass premium
      </button>
    </div>
  );
}
