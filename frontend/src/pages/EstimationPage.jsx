import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import './AppPages.css';

const formatCurrency = (value) => `${Math.round(Number(value || 0)).toLocaleString()} EUR`;

export default function EstimationPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    marque: '',
    modele: '',
    annee: '',
    kilometrage: '',
    carburant: 'essence',
    boite: 'manuelle',
    pays: 'DZ',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const onChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    try {
      const payload = {
        ...form,
        annee: Number(form.annee),
        kilometrage: Number(form.kilometrage),
      };
      const { data } = await axiosClient.post('/api/estimation/', payload);
      setResult(data);
    } catch {
      setError('Impossible de calculer l estimation.');
    } finally {
      setLoading(false);
    }
  };

  const confidence = useMemo(() => {
    if (!result) return null;
    const spread = Number(result.fourchette_haute || 0) - Number(result.fourchette_basse || 0);
    const center = Number(result.prix_estime || 1);
    const ratio = center > 0 ? 1 - Math.min(spread / center, 1) : 0;
    return Math.max(0, Math.round(ratio * 100));
  }, [result]);

  return (
    <div className="app-page">
      <div className="app-breadcrumb">
        <button type="button" onClick={() => navigate('/dashboard')}>Accueil</button>
        <span>&gt;</span>
        <span>Estimation</span>
      </div>

      <div className="app-header">
        <h1>Estimation ML</h1>
        <p>Calculez un prix cible et une fourchette intelligente pour chaque vehicule.</p>
      </div>

      <div className="app-grid-two">
        <article className="app-card">
          <h3>Parametres vehicule</h3>
          <p className="app-card-sub">Entrez les informations principales pour lancer l'analyse.</p>

          <form className="app-form" onSubmit={onSubmit}>
            <div className="app-form-grid">
              <input className="app-input" name="marque" value={form.marque} onChange={onChange} required placeholder="Marque" />
              <input className="app-input" name="modele" value={form.modele} onChange={onChange} required placeholder="Modele" />
              <input className="app-input" name="annee" type="number" value={form.annee} onChange={onChange} required placeholder="Annee" />
              <input className="app-input" name="kilometrage" type="number" value={form.kilometrage} onChange={onChange} required placeholder="Kilometrage" />
              <select className="app-select" name="carburant" value={form.carburant} onChange={onChange}>
                <option value="essence">Essence</option>
                <option value="diesel">Diesel</option>
                <option value="electrique">Electrique</option>
                <option value="hybride">Hybride</option>
              </select>
              <select className="app-select" name="boite" value={form.boite} onChange={onChange}>
                <option value="manuelle">Manuelle</option>
                <option value="automatique">Automatique</option>
              </select>
            </div>

            <button className="app-btn" type="submit" disabled={loading}>
              {loading ? 'Calcul en cours...' : 'Lancer estimation'}
            </button>
          </form>

          {error && <div className="app-error" style={{ marginTop: 10 }}>{error}</div>}
        </article>

        <article className="app-card">
          <h3>Resultat IA</h3>
          <p className="app-card-sub">Prix recommande avec lecture de confiance.</p>

          {!result && !loading && (
            <div className="app-empty">Aucun resultat pour le moment. Lancez une estimation.</div>
          )}

          {loading && <div className="app-loading">Analyse en cours...</div>}

          {result && (
            <div className="app-stack">
              <div className="app-kpi accent">
                <label>Prix estime</label>
                <strong>{formatCurrency(result.prix_estime)}</strong>
                <small>Valeur centrale calculee</small>
              </div>

              <div className="app-kpi">
                <label>Fourchette recommandee</label>
                <strong>{formatCurrency(result.fourchette_basse)} - {formatCurrency(result.fourchette_haute)}</strong>
                <small>Zone de negociation probable</small>
              </div>

              <div className="app-kpi good">
                <label>Indice confiance</label>
                <strong>{confidence ?? 0}%</strong>
                <small>Stabilite de prediction sur ce profil vehicule</small>
              </div>

              <button className="app-btn-ghost" type="button" onClick={() => navigate('/annonces')}>
                Comparer avec les annonces
              </button>
            </div>
          )}
        </article>
      </div>
    </div>
  );
}
