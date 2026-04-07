import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';

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
    } catch (err) {
      setError('Impossible de calculer l’estimation.');
    } finally {
      setLoading(false);
    }
  };

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
        <span style={{ color: '#8B8BA0' }}>Estimation</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>
        Estimation ML
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Estimez le prix juste d’un véhicule.
      </p>

      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 10, maxWidth: 560 }}>
        <input name="marque" value={form.marque} onChange={onChange} required placeholder="Marque" style={inputStyle} />
        <input name="modele" value={form.modele} onChange={onChange} required placeholder="Modèle" style={inputStyle} />
        <input name="annee" type="number" value={form.annee} onChange={onChange} required placeholder="Année" style={inputStyle} />
        <input name="kilometrage" type="number" value={form.kilometrage} onChange={onChange} required placeholder="Kilométrage" style={inputStyle} />
        <select name="carburant" value={form.carburant} onChange={onChange} style={inputStyle}>
          <option value="essence">Essence</option>
          <option value="diesel">Diesel</option>
          <option value="electrique">Électrique</option>
          <option value="hybride">Hybride</option>
        </select>
        <select name="boite" value={form.boite} onChange={onChange} style={inputStyle}>
          <option value="manuelle">Manuelle</option>
          <option value="automatique">Automatique</option>
        </select>
        <button type="submit" disabled={loading} style={buttonStyle}>
          {loading ? 'Calcul...' : 'Estimer'}
        </button>
      </form>

      {error && <p style={{ color: '#FCA5A5', marginTop: 12 }}>{error}</p>}

      {result && (
        <div style={{ marginTop: 18, background: '#13131E', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, padding: 14 }}>
          <div style={{ color: '#8B8BA0', fontSize: 12 }}>Prix estimé</div>
          <div style={{ color: '#6C63FF', fontSize: 30, fontWeight: 700 }}>
            {Number(result.prix_estime || 0).toLocaleString()} €
          </div>
          <div style={{ color: '#8B8BA0', fontSize: 13 }}>
            Fourchette: {Number(result.fourchette_basse || 0).toLocaleString()} € - {Number(result.fourchette_haute || 0).toLocaleString()} €
          </div>
        </div>
      )}
    </div>
  );
}

const inputStyle = {
  background: '#13131E',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#F0F0F5',
  padding: '10px 12px',
};

const buttonStyle = {
  border: 'none',
  borderRadius: 8,
  background: '#6C63FF',
  color: '#fff',
  padding: '10px 12px',
  cursor: 'pointer',
  fontWeight: 600,
};
