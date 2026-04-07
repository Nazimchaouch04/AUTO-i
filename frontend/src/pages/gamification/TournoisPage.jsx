import { useNavigate } from 'react-router-dom';

export default function TournoisPage() {
  const navigate = useNavigate();

  return (
    <div style={{ color: '#F0F0F5', padding: '0 0 32px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 24, fontSize: 13 }}>
        <span onClick={() => navigate('/dashboard')} style={{ color: '#6C63FF', cursor: 'pointer' }}>Accueil</span>
        <span style={{ color: '#8B8BA0' }}>›</span>
        <span style={{ color: '#8B8BA0' }}>Tournois</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>Tournois</h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Compétitions en direct.
      </p>

      <div style={{ background: '#13131E', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, padding: 12 }}>
        Les tournois seront disponibles dans une prochaine mise à jour.
      </div>
    </div>
  );
}
