import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import axiosClient from '../../api/axiosClient';
import {
  setCredentials,
  setError,
  setLoading,
} from '../../store/userSlice';
import './RegisterPage.css';

const validateUsername = (value) => {
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

const validateEmail = (value) => {
  const trimmed = value.trim();

  if (!trimmed) {
    return 'L email est obligatoire.';
  }

  if (trimmed.length > 254) {
    return 'L email est trop long.';
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!emailRegex.test(trimmed)) {
    return 'Format email invalide.';
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

const validatePasswordConfirm = (password, confirmation) => {
  if (!confirmation) {
    return 'La confirmation du mot de passe est obligatoire.';
  }

  if (password !== confirmation) {
    return 'Les mots de passe ne correspondent pas.';
  }

  return '';
};

const validateForm = (form) => ({
  username: validateUsername(form.username),
  email: validateEmail(form.email),
  password: validatePassword(form.password),
  password_confirm: validatePasswordConfirm(form.password, form.password_confirm),
});

const hasFieldErrors = (errors) => Object.values(errors).some(Boolean);

const touchedAll = {
  username: true,
  email: true,
  password: true,
  password_confirm: true,
};

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [fieldErrors, setFieldErrors] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [touched, setTouched] = useState({
    username: false,
    email: false,
    password: false,
    password_confirm: false,
  });

  const { loading, error } = useSelector((s) => s.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const updateAllErrors = (nextForm) => {
    setFieldErrors(validateForm(nextForm));
  };

  const onChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => {
      const next = { ...prev, [name]: value };

      if (touched[name] || touched.password || touched.password_confirm) {
        updateAllErrors(next);
      }

      return next;
    });
  };

  const onBlur = (field) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    updateAllErrors(form);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(setError(null));

    const payload = {
      ...form,
      username: form.username.trim(),
      email: form.email.trim(),
    };

    const errors = validateForm(payload);
    setTouched(touchedAll);
    setFieldErrors(errors);

    if (hasFieldErrors(errors)) {
      return;
    }

    dispatch(setLoading(true));

    try {
      const { data } = await axiosClient.post('/api/auth/register/', payload);

      if (data.access && data.refresh) {
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
            user: profileData?.user || data.user_data || {
              username: payload.username,
              email: payload.email,
            },
            profil: profileData?.profil || data.profil_data || null,
            abonnement: profileData?.abonnement || null,
            access: data.access,
            refresh: data.refresh,
          }),
        );

        navigate('/dashboard', { replace: true });
        return;
      }

      navigate('/login', { replace: true });
    } catch (err) {
      const responsePayload = err?.response?.data;
      const message = responsePayload?.detail
        || responsePayload?.email?.[0]
        || responsePayload?.username?.[0]
        || responsePayload?.password?.[0]
        || responsePayload?.password_confirm?.[0]
        || 'Inscription impossible';

      dispatch(setError(message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const fieldError = (name) => touched[name] && fieldErrors[name];

  return (
    <div className="register-page">
      <div className="register-track-bg" />

      <div className="register-layout">
        <section className="register-card">
          <h1>Inscription</h1>
          <p className="register-subtitle">Creez un compte AutoIntel.</p>

          {error && <div className="register-alert-error">{error}</div>}

          <form onSubmit={handleSubmit} noValidate className="register-form">
            <div className="register-field-wrap">
              <input
                name="username"
                type="text"
                placeholder="Username"
                value={form.username}
                onChange={onChange}
                onBlur={() => onBlur('username')}
                autoComplete="username"
                aria-invalid={!!fieldError('username')}
                className={`register-input ${fieldError('username') ? 'is-invalid' : ''}`}
              />
              {fieldError('username') && (
                <span className="register-field-error">{fieldErrors.username}</span>
              )}
            </div>

            <div className="register-field-wrap">
              <input
                name="email"
                type="text"
                placeholder="Email"
                value={form.email}
                onChange={onChange}
                onBlur={() => onBlur('email')}
                autoComplete="email"
                aria-invalid={!!fieldError('email')}
                className={`register-input ${fieldError('email') ? 'is-invalid' : ''}`}
              />
              {fieldError('email') && (
                <span className="register-field-error">{fieldErrors.email}</span>
              )}
            </div>

            <div className="register-field-wrap">
              <input
                name="password"
                type="password"
                placeholder="Mot de passe"
                value={form.password}
                onChange={onChange}
                onBlur={() => onBlur('password')}
                autoComplete="new-password"
                aria-invalid={!!fieldError('password')}
                className={`register-input ${fieldError('password') ? 'is-invalid' : ''}`}
              />
              {fieldError('password') && (
                <span className="register-field-error">{fieldErrors.password}</span>
              )}
            </div>

            <div className="register-field-wrap">
              <input
                name="password_confirm"
                type="password"
                placeholder="Confirmez le mot de passe"
                value={form.password_confirm}
                onChange={onChange}
                onBlur={() => onBlur('password_confirm')}
                autoComplete="new-password"
                aria-invalid={!!fieldError('password_confirm')}
                className={`register-input ${fieldError('password_confirm') ? 'is-invalid' : ''}`}
              />
              {fieldError('password_confirm') && (
                <span className="register-field-error">{fieldErrors.password_confirm}</span>
              )}
            </div>

            <button type="submit" disabled={loading} className="register-submit-btn">
              {loading ? 'Creation...' : 'Creer le compte'}
            </button>
          </form>

          <p className="register-login-link">
            Deja inscrit ? <Link to="/login">Se connecter</Link>
          </p>
        </section>

        <section className="register-showcase" aria-hidden="true">
          <div className="register-tacho-wrap">
            <div className="register-shift-lights">
              <span className="shift-light" />
              <span className="shift-light" />
              <span className="shift-light" />
              <span className="shift-light" />
              <span className="shift-light" />
            </div>

            <div className="register-tachometer">
              <div className="register-tacho-ring" />
              <div className="register-tacho-redzone" />

              <div className="register-tacho-marks">
                <span>1</span>
                <span>2</span>
                <span>3</span>
                <span>4</span>
                <span>5</span>
                <span>6</span>
                <span>7</span>
                <span className="warn">8</span>
                <span className="warn">9</span>
              </div>

              <div className="register-needle-pivot">
                <span className="register-needle" />
              </div>

              <div className="register-tacho-center">
                <strong>8.4</strong>
                <small>x1000 RPM</small>
                <em>SPORT ENGINE</em>
              </div>
            </div>
          </div>

          <div className="register-chip-row">
            <span className="register-chip">Tracking annonces</span>
            <span className="register-chip">Detection tendances</span>
            <span className="register-chip">Alertes instantanees</span>
          </div>

          <div className="register-steps">
            <div className="register-step">
              <strong>01</strong>
              <span>Creation de compte</span>
            </div>
            <div className="register-step">
              <strong>02</strong>
              <span>Activation profil auto</span>
            </div>
            <div className="register-step">
              <strong>03</strong>
              <span>Demarrage des analyses</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
