import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import axiosClient from '../../api/axiosClient';
import {
  setCredentials,
  setError,
  setLoading,
} from '../../store/userSlice';
import './LoginPage.css';

const validateIdentifier = (value) => {
  const trimmed = value.trim();

  if (!trimmed) {
    return 'Le nom utilisateur est obligatoire.';
  }

  if (trimmed.length < 3) {
    return 'Le nom utilisateur doit contenir au moins 3 caracteres.';
  }

  if (trimmed.length > 150) {
    return 'Le nom utilisateur est trop long.';
  }

  if (/\s/.test(trimmed)) {
    return 'Le nom utilisateur ne doit pas contenir d espace.';
  }

  return '';
};

const validatePassword = (value) => {
  if (!value) {
    return 'Le mot de passe est obligatoire.';
  }

  if (value.length < 6) {
    return 'Le mot de passe doit contenir au moins 6 caracteres.';
  }

  if (value.length > 128) {
    return 'Le mot de passe est trop long.';
  }

  return '';
};

const validateForm = ({ identifier, password }) => ({
  identifier: validateIdentifier(identifier),
  password: validatePassword(password),
});

export default function LoginPage() {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [fieldErrors, setFieldErrors] = useState({
    identifier: '',
    password: '',
  });
  const [touched, setTouched] = useState({
    identifier: false,
    password: false,
  });

  const { loading, error } = useSelector((s) => s.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const updateFieldError = (field, value) => {
    const nextError =
      field === 'identifier' ? validateIdentifier(value) : validatePassword(value);
    setFieldErrors((prev) => ({ ...prev, [field]: nextError }));
  };

  const hasFieldErrors = (errors) => Object.values(errors).some(Boolean);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(setError(null));

    const errors = validateForm({ identifier, password });
    setTouched({ identifier: true, password: true });
    setFieldErrors(errors);

    if (hasFieldErrors(errors)) {
      return;
    }

    dispatch(setLoading(true));

    try {
      const { data } = await axiosClient.post('/api/auth/login/', {
        username: identifier.trim(),
        password,
      });

      let profileData = null;
      try {
        const profileRes = await axiosClient.get('/api/auth/profile/', {
          headers: { Authorization: `Bearer ${data.access}` },
        });
        profileData = profileRes.data;
      } catch {
        profileData = null;
      }

      dispatch(
        setCredentials({
          user: profileData?.user || data.user_data || { username: identifier.trim() },
          profil: profileData?.profil || data.profil_data || null,
          abonnement: profileData?.abonnement || null,
          access: data.access,
          refresh: data.refresh,
        }),
      );

      navigate(from, { replace: true });
    } catch (err) {
      const message = err?.response?.data?.detail || 'Connexion echouee';
      dispatch(setError(message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <div className="login-page">
      <div className="login-orb login-orb-a" />
      <div className="login-orb login-orb-b" />

      <div className="login-layout">
        <section className="login-showcase" aria-hidden="true">
          <span className="login-kicker">Track Mode AI</span>
          <h2>Prenez la route des bonnes decisions automobiles.</h2>
          <p>
            Analyse en temps reel, score marche et alertes intelligentes pour acheter
            et vendre avec plus de confiance.
          </p>

          <div className="login-speed-card">
            <div className="login-speed-dial">
              <span className="login-speed-needle" />
              <span className="login-speed-core" />
            </div>
            <div className="login-speed-meta">
              <strong>Precision moteur IA</strong>
              <span>96.2% sur les estimations recentes</span>
            </div>
          </div>

          <div className="login-market-feed">
            <div className="login-feed-item">
              <span>BMW Serie 3 2021</span>
              <strong>Offre attractive</strong>
            </div>
            <div className="login-feed-item">
              <span>Peugeot 3008 2020</span>
              <strong>Prix stable</strong>
            </div>
            <div className="login-feed-item">
              <span>Mercedes C220 2019</span>
              <strong>Alerte active</strong>
            </div>
          </div>

          <div className="login-road">
            <span />
          </div>
        </section>

        <section className="login-card">
          <h1>Connexion</h1>
          <p className="login-subtitle">Connectez-vous pour acceder a AutoIntel.</p>

          {error && <div className="login-alert-error">{error}</div>}

          <form onSubmit={handleSubmit} noValidate className="login-form">
            <div className="login-field-wrap">
              <input
                type="text"
                placeholder="Username"
                value={identifier}
                onChange={(e) => {
                  const value = e.target.value;
                  setIdentifier(value);
                  if (touched.identifier) {
                    updateFieldError('identifier', value);
                  }
                }}
                onBlur={() => {
                  setTouched((prev) => ({ ...prev, identifier: true }));
                  updateFieldError('identifier', identifier);
                }}
                autoComplete="username"
                aria-invalid={touched.identifier && !!fieldErrors.identifier}
                className={`login-input ${
                  touched.identifier && fieldErrors.identifier ? 'is-invalid' : ''
                }`}
              />
              {touched.identifier && fieldErrors.identifier && (
                <span className="login-field-error">{fieldErrors.identifier}</span>
              )}
            </div>

            <div className="login-field-wrap">
              <input
                type="password"
                placeholder="Mot de passe"
                value={password}
                onChange={(e) => {
                  const value = e.target.value;
                  setPassword(value);
                  if (touched.password) {
                    updateFieldError('password', value);
                  }
                }}
                onBlur={() => {
                  setTouched((prev) => ({ ...prev, password: true }));
                  updateFieldError('password', password);
                }}
                autoComplete="current-password"
                aria-invalid={touched.password && !!fieldErrors.password}
                className={`login-input ${
                  touched.password && fieldErrors.password ? 'is-invalid' : ''
                }`}
              />
              {touched.password && fieldErrors.password && (
                <span className="login-field-error">{fieldErrors.password}</span>
              )}
            </div>

            <button type="submit" disabled={loading} className="login-submit-btn">
              {loading ? 'Connexion...' : 'Se connecter'}
            </button>
          </form>

          <p className="login-register-link">
            Pas de compte ?{' '}
            <Link to="/register">
              S'inscrire
            </Link>
          </p>
        </section>
      </div>
    </div>
  );
}
