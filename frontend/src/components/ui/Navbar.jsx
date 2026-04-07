import { useLocation, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const TITRES = {
  '/dashboard': ['Dashboard', "Vue d'ensemble du marché"],
  '/annonces': ['Annonces', 'Toutes les annonces automobiles'],
  '/estimation': ['Estimation ML', 'Estimez le prix juste'],
  '/alertes': ['Mes alertes', 'Suivi automatique du marché'],
  '/profil': ['Mon profil', 'Statistiques et progression'],
  '/abonnement': ['Abonnement', 'Gérer mon plan'],
  '/classement': ['Classement', 'Top joueurs AutoIntel'],
  '/defis': ['Défis', 'Complète tes objectifs'],
  '/battles': ['Battles 1v1', "Affronte d'autres joueurs"],
  '/tournois': ['Tournois', 'Compétitions en direct'],
  '/collection': ['Collection', 'Tes Car DNA Cards'],
  '/season-pass': ['Season Pass', 'Racing Edition · Saison 1'],
  '/boutique': ['Boutique', 'Dépense tes AutoCoins'],
};

export default function Navbar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { profil } = useSelector((s) => s.user);

  const basePath = `/${pathname.split('/')[1]}`;
  const [titre, sousTitre] = TITRES[basePath] || ['AutoIntel', ''];

  return (
    <header
      style={{
        height: 60,
        background: 'rgba(13,13,20,0.85)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 28px',
        flexShrink: 0,
      }}
    >
      {/* Titre page */}
      <div>
        <div
          style={{
            color: '#F0F0F5',
            fontSize: 16,
            fontWeight: 500,
            lineHeight: 1.2,
          }}
        >
          {titre}
        </div>
        {sousTitre && (
          <div style={{ color: '#8B8BA0', fontSize: 12 }}>
            {sousTitre}
          </div>
        )}
      </div>

      {/* Actions droite */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        {/* Bouton estimation rapide */}
        <button
          onClick={() => navigate('/estimation')}
          style={{
            background: '#6C63FF',
            color: '#fff',
            border: 'none',
            borderRadius: 7,
            padding: '7px 14px',
            fontSize: 13,
            fontWeight: 500,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 5,
          }}
        >
          🎯 Estimer
        </button>

        {/* Badge AutoCoin */}
        <div
          onClick={() => navigate('/boutique')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 5,
            background: 'rgba(245,158,11,0.08)',
            border: '1px solid rgba(245,158,11,0.2)',
            borderRadius: 16,
            padding: '5px 11px',
            cursor: 'pointer',
          }}
        >
          <span style={{ fontSize: 14 }}>🪙</span>
          <span
            style={{
              color: '#F59E0B',
              fontWeight: 600,
              fontSize: 14,
            }}
          >
            {profil?.autocoin_balance ?? 0}
          </span>
          <span style={{ color: '#8B8BA0', fontSize: 11 }}>AC</span>
        </div>

        {/* Alertes */}
        <div
          onClick={() => navigate('/alertes')}
          style={{ cursor: 'pointer', fontSize: 18 }}
        >
          🔔
        </div>

        {/* Avatar */}
        <div
          onClick={() => navigate('/profil')}
          style={{
            width: 34,
            height: 34,
            borderRadius: '50%',
            background: '#6C63FF',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: 700,
            fontSize: 13,
            border: '2px solid rgba(108,99,255,0.3)',
          }}
        >
          {profil?.username?.[0]?.toUpperCase() || 'U'}
        </div>
      </div>
    </header>
  );
}
