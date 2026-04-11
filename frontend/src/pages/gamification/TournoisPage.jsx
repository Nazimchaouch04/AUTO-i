import { useNavigate } from 'react-router-dom';
import '../AppPages.css';

const tournois = [
  { nom: 'Sprint Night Cup', date: 'Vendredi 21:00', format: 'Elimination', reward: '1200 XP + 450 AC' },
  { nom: 'Dealer Challenge', date: 'Samedi 18:00', format: 'Round robin', reward: '900 XP + 300 AC' },
  { nom: 'Elite Price Wars', date: 'Dimanche 20:30', format: 'Final 1v1', reward: '2000 XP + badge Elite' },
];

export default function TournoisPage() {
  const navigate = useNavigate();

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Tournois</span>
      </div>

      <div className="app-header">
        <h1>Tournois</h1>
        <p>Calendrier competitif et recompenses de saison.</p>
      </div>

      <div className="app-grid-three" style={{ marginBottom: 12 }}>
        <div className="app-kpi accent">
          <label>Evenements cette semaine</label>
          <strong>{tournois.length}</strong>
          <small>Sessions deja annoncees</small>
        </div>
        <div className="app-kpi good">
          <label>Record perso</label>
          <strong>#12</strong>
          <small>Meilleur rang atteint</small>
        </div>
        <div className="app-kpi warn">
          <label>Objectif saison</label>
          <strong>Top 10</strong>
          <small>Montee de division</small>
        </div>
      </div>

      <div className="app-stack">
        {tournois.map((t) => (
          <article key={t.nom} className="app-list-item">
            <div>
              <div className="app-list-title">{t.nom}</div>
              <div className="app-list-meta">{t.date} - Format {t.format}</div>
            </div>
            <div>
              <span className="app-badge">{t.reward}</span>
            </div>
          </article>
        ))}
      </div>

      <div className="app-grid-half" style={{ marginTop: 12 }}>
        <button className="app-btn-ghost" type="button" onClick={() => navigate('/battles')}>
          S'entrainer en battle
        </button>
        <button className="app-btn-ghost" type="button" onClick={() => navigate('/classement')}>
          Voir le classement live
        </button>
      </div>
    </div>
  );
}
