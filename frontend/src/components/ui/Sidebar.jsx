import { NavLink, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

const MENU = [
  {
    titre: 'Principal',
    items: [
      { path: '/dashboard', label: 'Dashboard', icon: '▦' },
      { path: '/annonces', label: 'Annonces', icon: '🚗' },
      { path: '/estimation', label: 'Estimation', icon: '🎯' },
      { path: '/alertes', label: 'Alertes', icon: '🔔' },
    ],
  },
  {
    titre: 'Gamification',
    items: [
      { path: '/classement', label: 'Classement', icon: '🏆' },
      { path: '/defis', label: 'Défis', icon: '⚡' },
      { path: '/battles', label: 'Battles 1v1', icon: '⚔️' },
      { path: '/tournois', label: 'Tournois', icon: '🏁' },
      { path: '/collection', label: 'Collection', icon: '🃏' },
      { path: '/season-pass', label: 'Season Pass', icon: '🎟️' },
      { path: '/boutique', label: 'Boutique', icon: '🛍️' },
    ],
  },
  {
    titre: 'Compte',
    items: [
      { path: '/profil', label: 'Mon profil', icon: '👤' },
      { path: '/abonnement', label: 'Abonnement', icon: '💎' },
    ],
  },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user, profil } = useSelector((s) => s.user);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    dispatch({ type: 'user/logout' });
    navigate('/login');
  };

  return (
    <aside
      style={{
        width: 252,
        background: '#13131E',
        borderRight: '1px solid rgba(255,255,255,0.06)',
        display: 'flex',
        flexDirection: 'column',
        flexShrink: 0,
        overflowY: 'auto',
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: '20px 18px 14px',
          borderBottom: '1px solid rgba(255,255,255,0.06)',
          cursor: 'pointer',
        }}
        onClick={() => navigate('/dashboard')}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 9,
          }}
        >
          <span style={{ fontSize: 20 }}>⚡</span>
          <span
            style={{
              color: '#6C63FF',
              fontWeight: 700,
              fontSize: 17,
              letterSpacing: '-0.3px',
            }}
          >
            AutoIntel
          </span>
        </div>
        <div style={{ color: '#8B8BA0', fontSize: 11, marginTop: 3 }}>
          Intelligence automobile
        </div>
      </div>

      {/* Navigation */}
      <nav style={{ flex: 1, padding: '10px 0' }}>
        {MENU.map((group) => (
          <div key={group.titre} style={{ marginBottom: 4 }}>
            <div
              style={{
                color: '#8B8BA0',
                fontSize: 10,
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: 1,
                padding: '10px 18px 4px',
              }}
            >
              {group.titre}
            </div>
            {group.items.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                style={({ isActive }) => ({
                  display: 'flex',
                  alignItems: 'center',
                  gap: 9,
                  padding: '8px 18px',
                  textDecoration: 'none',
                  fontSize: 13,
                  color: isActive ? '#F0F0F5' : '#8B8BA0',
                  background: isActive ? 'rgba(108,99,255,0.1)' : 'transparent',
                  borderLeft: isActive ? '3px solid #6C63FF' : '3px solid transparent',
                  transition: 'all 150ms',
                })}
              >
                <span style={{ fontSize: 14 }}>{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* Profil bas */}
      <div
        style={{
          padding: '14px 18px',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}
      >
        <div
          onClick={() => navigate('/profil')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 9,
            marginBottom: 10,
            cursor: 'pointer',
          }}
        >
          <div
            style={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              background: '#6C63FF',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              fontWeight: 700,
              fontSize: 13,
              flexShrink: 0,
            }}
          >
            {user?.username?.[0]?.toUpperCase() || 'U'}
          </div>
          <div style={{ minWidth: 0 }}>
            <div
              style={{
                color: '#F0F0F5',
                fontSize: 13,
                fontWeight: 500,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {user?.username || 'Utilisateur'}
            </div>
            <div style={{ color: '#6C63FF', fontSize: 11 }}>
              {profil?.nom_niveau || 'Apprenti'}
            </div>
          </div>
        </div>

        {/* XP bar */}
        <div style={{ marginBottom: 10 }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: 4,
            }}
          >
            <span style={{ color: '#8B8BA0', fontSize: 10 }}>
              Niveau {profil?.niveau || 1}
            </span>
            <span style={{ color: '#8B8BA0', fontSize: 10 }}>
              {profil?.xp || 0} XP
            </span>
          </div>
          <div
            style={{
              height: 4,
              background: 'rgba(255,255,255,0.08)',
              borderRadius: 2,
            }}
          >
            <div
              style={{
                height: '100%',
                width: `${Math.min(profil?.progression_pct || 0, 100)}%`,
                background: '#6C63FF',
                borderRadius: 2,
                transition: 'width 1s ease',
              }}
            />
          </div>
        </div>

        <button
          onClick={handleLogout}
          style={{
            width: '100%',
            padding: '6px',
            background: 'transparent',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: 6,
            color: '#8B8BA0',
            fontSize: 12,
            cursor: 'pointer',
          }}
        >
          Déconnexion
        </button>
      </div>
    </aside>
  );
}
