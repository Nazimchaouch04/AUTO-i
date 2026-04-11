import { useNavigate } from 'react-router-dom';
import '../AppPages.css';

const cards = [
  { id: 1, nom: 'DNA Turbo', rarete: 'Rare', set: 'Performance' },
  { id: 2, nom: 'Collector GT', rarete: 'Epic', set: 'Legends' },
  { id: 3, nom: 'Hybrid Pulse', rarete: 'Common', set: 'Eco Drive' },
  { id: 4, nom: 'Track Dominator', rarete: 'Legendary', set: 'Racing' },
  { id: 5, nom: 'Urban Sensor', rarete: 'Common', set: 'City' },
  { id: 6, nom: 'Drift Master', rarete: 'Rare', set: 'Racing' },
];

const rarityTone = {
  Common: '',
  Rare: 'app-pill-good',
  Epic: 'app-pill-warn',
  Legendary: 'app-pill-danger',
};

export default function CollectionPage() {
  const navigate = useNavigate();

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Collection</span>
      </div>

      <div className="app-header">
        <h1>Collection Car DNA</h1>
        <p>Cartes obtenues via defis, battles et tournois.</p>
      </div>

      <div className="app-grid-three" style={{ marginBottom: 12 }}>
        <div className="app-kpi accent">
          <label>Cartes debloquees</label>
          <strong>{cards.length}</strong>
          <small>Sur 120 cartes saison</small>
        </div>
        <div className="app-kpi good">
          <label>Sets complets</label>
          <strong>2</strong>
          <small>Bonus actifs</small>
        </div>
        <div className="app-kpi warn">
          <label>Legendaires</label>
          <strong>{cards.filter((c) => c.rarete === 'Legendary').length}</strong>
          <small>Objets premium obtenus</small>
        </div>
      </div>

      <div className="app-grid-cards">
        {cards.map((card) => (
          <article key={card.id} className="app-card">
            <h3>{card.nom}</h3>
            <p className="app-card-sub">Set: {card.set}</p>
            <div className="app-chip-row" style={{ marginTop: 10 }}>
              <span className={`app-badge ${rarityTone[card.rarete] || ''}`}>{card.rarete}</span>
              <span className="app-badge">DNA #{String(card.id).padStart(3, '0')}</span>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
