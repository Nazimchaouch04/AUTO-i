import { Link } from 'react-router-dom';
import './LandingPage.css';

const stats = [
  { value: '48k+', label: 'annonces analysees / mois' },
  { value: '96%', label: 'precision moyenne des estimations' },
  { value: '< 3s', label: 'temps moyen pour une estimation' },
  { value: '24/7', label: 'surveillance du marche en continu' },
];

const features = [
  {
    icon: 'AI',
    title: 'Estimation intelligente',
    text: 'Un prix cible avec fourchette, score de confiance, et contexte du marche local.',
  },
  {
    icon: 'AL',
    title: 'Alertes ultra ciblees',
    text: 'Filtrez par budget, kilometrage, marque et recevez les nouvelles annonces en direct.',
  },
  {
    icon: 'BI',
    title: 'Dashboard actionnable',
    text: 'Tendances, evolution des prix, meilleures opportunites et signaux de surcote.',
  },
  {
    icon: 'XP',
    title: 'Experience gamifiee',
    text: 'Defis, classements et recompenses pour rendre vos analyses plus engageantes.',
  },
];

const steps = [
  { index: '01', title: 'Connectez votre compte', text: 'Creation rapide et acces immediat aux modules AutoIntel.' },
  { index: '02', title: 'Lancez vos analyses', text: 'Comparez des vehicules et estimez leur juste valeur en un clic.' },
  { index: '03', title: 'Activez vos alertes', text: 'Soyez notifie des que le marche propose une meilleure opportunite.' },
];

export default function LandingPage() {
  return (
    <div className="landing-root">
      <div className="landing-aurora landing-aurora-one" />
      <div className="landing-aurora landing-aurora-two" />
      <div className="landing-grid-overlay" />

      <header className="landing-shell landing-header">
        <Link to="/" className="landing-logo">
          <span className="landing-logo-mark">⚡</span>
          <span className="landing-logo-text">AutoIntel</span>
        </Link>

        <nav className="landing-nav">
          <Link to="/login" className="landing-btn landing-btn-ghost">
            Connexion
          </Link>
          <Link to="/register" className="landing-btn landing-btn-primary">
            Essai gratuit
          </Link>
        </nav>
      </header>

      <main className="landing-shell landing-main">
        <section className="landing-hero">
          <div className="landing-hero-copy">
            <span className="landing-kicker reveal reveal-1">
              Intelligence automobile de nouvelle generation
            </span>
            <h1 className="landing-title reveal reveal-2">
              Trouvez plus vite les bonnes affaires auto, sans decider a l&apos;aveugle
            </h1>
            <p className="landing-subtitle reveal reveal-3">
              AutoIntel combine machine learning, tracking d&apos;annonces et dashboard
              decisionnel pour estimer, comparer et agir au bon moment.
            </p>

            <div className="landing-actions reveal reveal-4">
              <Link to="/register" className="landing-btn landing-btn-primary landing-btn-big">
                Demarrer maintenant
              </Link>
              <Link to="/login" className="landing-btn landing-btn-ghost landing-btn-big">
                Acceder a mon compte
              </Link>
            </div>

            <div className="landing-proof reveal reveal-5">
              <span className="landing-proof-dot" />
              Donnees temps reel, mises a jour en continu, pour particuliers et pros.
            </div>
          </div>

          <div className="landing-hero-panel reveal reveal-4">
            <div className="landing-panel-head">
              <span className="landing-pulse" />
              Flux live AutoIntel
            </div>
            <div className="landing-panel-list">
              <div className="landing-panel-item">
                <span>BMW Serie 3 2021</span>
                <strong>Score +18%</strong>
              </div>
              <div className="landing-panel-item">
                <span>Peugeot 3008 2020</span>
                <strong>Prix ideal detecte</strong>
              </div>
              <div className="landing-panel-item">
                <span>Mercedes C220 2019</span>
                <strong>Alerte: offre sous-cotee</strong>
              </div>
            </div>
            <div className="landing-panel-foot">
              <span>12 analyses executees aujourd&apos;hui</span>
              <Link to="/register">Activer les alertes</Link>
            </div>
          </div>
        </section>

        <section className="landing-stats">
          {stats.map((item, idx) => (
            <article
              key={item.label}
              className="landing-stat-card"
              style={{ '--delay': `${idx * 120}ms` }}
            >
              <strong>{item.value}</strong>
              <span>{item.label}</span>
            </article>
          ))}
        </section>

        <section className="landing-section">
          <div className="landing-section-head">
            <h2>Tout ce qu&apos;il faut pour mieux acheter et mieux vendre</h2>
            <p>
              Une experience complete: prediction de prix, suivi de marche et navigation
              orientee performance.
            </p>
          </div>

          <div className="landing-feature-grid">
            {features.map((item, idx) => (
              <article
                key={item.title}
                className="landing-feature-card"
                style={{ '--delay': `${idx * 100}ms` }}
              >
                <div className="landing-feature-icon">{item.icon}</div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section">
          <div className="landing-section-head">
            <h2>Comment ca marche</h2>
            <p>Trois etapes simples pour passer de la recherche a la decision.</p>
          </div>

          <div className="landing-steps">
            {steps.map((step, idx) => (
              <article
                key={step.index}
                className="landing-step-card"
                style={{ '--delay': `${idx * 140}ms` }}
              >
                <span className="landing-step-index">{step.index}</span>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-cta">
          <h2>Pret a prendre de meilleures decisions auto ?</h2>
          <p>
            Rejoignez AutoIntel et profitez d&apos;une plateforme rapide, lisible et
            concentree sur l&apos;action.
          </p>
          <div className="landing-actions">
            <Link to="/register" className="landing-btn landing-btn-primary landing-btn-big">
              Creer un compte
            </Link>
            <Link to="/login" className="landing-btn landing-btn-ghost landing-btn-big">
              Se connecter
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
