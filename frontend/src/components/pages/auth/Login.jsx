import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { loginUser, clearError } from '../../../store/userSlice';
import { Loader2, AlertCircle, Mail, Lock } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState(localStorage.getItem('remembered_email') || '');
  const [password, setPassword] = useState('');
  const [shake, setShake] = useState(false);

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { loading, error, isAuthenticated } = useSelector((state) => state.user);

  const from = location.state?.from?.pathname || '/dashboard';

  useEffect(() => {
    dispatch(clearError());
    if (isAuthenticated) navigate(from, { replace: true });
  }, [dispatch, isAuthenticated, navigate, from]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    localStorage.setItem('remembered_email', email);
    const resultAction = await dispatch(loginUser({ email, password }));
    if (loginUser.rejected.match(resultAction)) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden" 
         style={{ background: '#0D0D1A' }}>
      
      {/* Background elements */}
      <div style={{ position: 'absolute', top: '-10%', left: '-10%', width: '40vw', height: '40vw', background: 'radial-gradient(circle, rgba(108,99,255,0.15) 0%, rgba(13,13,26,0) 70%)', zIndex: 0 }} />
      <div style={{ position: 'absolute', bottom: '-20%', right: '-10%', width: '60vw', height: '60vw', background: 'radial-gradient(circle, rgba(0,212,170,0.1) 0%, rgba(13,13,26,0) 70%)', zIndex: 0 }} />

      <div style={{
        position: 'relative', zIndex: 1, width: '100%', maxWidth: 420, padding: 40,
        background: 'rgba(19, 19, 30, 0.7)', backdropFilter: 'blur(20px)',
        border: '1px solid rgba(108, 99, 255, 0.2)', borderRadius: 24,
        boxShadow: '0 20px 40px rgba(0,0,0,0.4)',
        animation: shake ? 'shake 0.5s cubic-bezier(.36,.07,.19,.97) both' : 'fadeInUp 0.6s ease-out'
      }}>
        
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <h1 style={{ fontSize: 32, fontWeight: 800, color: '#fff', margin: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
            <span style={{ color: '#6C63FF' }}>Auto</span>Intel
          </h1>
          <p style={{ color: '#8888AA', marginTop: 8, fontSize: 14 }}>Analysez le marché automobile</p>
        </div>

        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #EF4444', color: '#FCA5A5', padding: '12px 16px', borderRadius: 12, marginBottom: 24, fontSize: 13, display: 'flex', alignItems: 'center', gap: 10 }}>
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          
          <div>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#F0F0F5', marginBottom: 8 }}>Adresse email</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#55557A' }}>
                <Mail size={18} />
              </div>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="jean.dupont@email.com"
                style={{
                  width: '100%', padding: '14px 14px 14px 44px', borderRadius: 12,
                  background: 'rgba(0,0,0,0.2)', border: '1px solid #2a2a3e', color: '#fff', fontSize: 15,
                  outline: 'none', transition: 'all 0.2s'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6C63FF'}
                onBlur={(e) => e.target.style.borderColor = '#2a2a3e'}
              />
            </div>
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <label style={{ fontSize: 13, fontWeight: 600, color: '#F0F0F5' }}>Mot de passe</label>
              <Link to="#" style={{ fontSize: 12, color: '#6C63FF', textDecoration: 'none' }}>Mot de passe oublié ?</Link>
            </div>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#55557A' }}>
                <Lock size={18} />
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                style={{
                  width: '100%', padding: '14px 14px 14px 44px', borderRadius: 12,
                  background: 'rgba(0,0,0,0.2)', border: '1px solid #2a2a3e', color: '#fff', fontSize: 15,
                  outline: 'none', transition: 'all 0.2s'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6C63FF'}
                onBlur={(e) => e.target.style.borderColor = '#2a2a3e'}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '16px', borderRadius: 12, border: 'none', cursor: loading ? 'not-allowed' : 'pointer',
              background: 'linear-gradient(135deg, #6C63FF, #9B59B6)', color: '#fff', fontWeight: 700, fontSize: 15,
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
              boxShadow: '0 8px 24px rgba(108, 99, 255, 0.3)', transition: 'all 0.2s', marginTop: 10,
              opacity: loading ? 0.7 : 1, transform: 'scale(1)'
            }}
            onMouseEnter={(e) => { if(!loading) e.currentTarget.style.transform = 'scale(1.02)' }}
            onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)' }}
          >
            {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> : null}
            {loading ? 'Connexion...' : 'Se connecter'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: 32 }}>
          <p style={{ color: '#8888AA', fontSize: 13 }}>
            Pas encore de compte ?{' '}
            <Link to="/register" style={{ color: '#fff', fontWeight: 600, textDecoration: 'none' }}>
              S'inscrire →
            </Link>
          </p>
        </div>

      </div>

      <style>{`
        @keyframes shake {
          10%, 90% { transform: translate3d(-1px, 0, 0); }
          20%, 80% { transform: translate3d(2px, 0, 0); }
          30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
          40%, 60% { transform: translate3d(4px, 0, 0); }
        }
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

export default Login;
