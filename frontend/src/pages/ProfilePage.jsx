import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import { useDispatch } from 'react-redux';
import { updateProfil } from '../store/userSlice';

export default function ProfilePage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await axiosClient.get('/api/auth/profile/');
        setProfile(data);
        if (data?.profil) dispatch(updateProfil(data.profil));
      } catch (err) {
        setError('Impossible de charger le profil.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [dispatch]);

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
        <span style={{ color: '#8B8BA0' }}>Mon profil</span>
      </div>

      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: 8 }}>
        Mon profil
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14, marginBottom: 24 }}>
        Statistiques et progression.
      </p>

      {loading && <p style={{ color: '#8B8BA0' }}>Chargement du profil...</p>}
      {!loading && error && <p style={{ color: '#FCA5A5' }}>{error}</p>}

      {!loading && !error && (
        <div
          style={{
            background: '#13131E',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: 10,
            padding: 14,
            display: 'grid',
            gap: 8,
          }}
        >
          <div>Username: <b>{profile?.user?.username || 'N/A'}</b></div>
          <div>Email: <b>{profile?.user?.email || 'N/A'}</b></div>
          <div>XP: <b>{profile?.profil?.xp ?? 0}</b></div>
          <div>Niveau: <b>{profile?.profil?.niveau ?? 1}</b></div>
          <div>AutoCoins: <b>{profile?.profil?.autocoin_balance ?? 0}</b></div>
        </div>
      )}
    </div>
  );
}
