import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser, clearError } from '../../../store/userSlice';
import { Loader2, AlertCircle, Mail, Lock, User, CheckCircle2 } from 'lucide-react';
import confetti from 'canvas-confetti';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: ''
  });
  
  const [shake, setShake] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.user);

  // Validation
  const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email);
  const isPassValid = formData.password.length >= 8;
  const isPassMatch = isPassValid && formData.password === formData.password_confirm;
  
  const isValid = formData.username.length >= 3 && isEmailValid && isPassMatch;

  // Password strength logic (simple)
  let passStrength = 0;
  if(formData.password.length > 0) passStrength = 1;
  if(formData.password.length >= 8) passStrength = 2;
  if(formData.password.length >= 8 && /[A-Z]/.test(formData.password) && /[0-9]/.test(formData.password)) passStrength = 3;

  const strengthColor = passStrength === 1 ? '#EF4444' : passStrength === 2 ? '#F59E0B' : passStrength === 3 ? '#10B981' : '#2a2a3e';

  useEffect(() => {
    dispatch(clearError());
  }, [dispatch]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isValid) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
      return;
    }

    const { password_confirm, ...submitData } = formData;
    submitData.password_confirm = password_confirm;

    const resultAction = await dispatch(registerUser(submitData));
    if (registerUser.rejected.match(resultAction)) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
    } else {
      // Success
      setSuccessMsg("Bienvenue ! 100 AC offerts");
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#6C63FF', '#00D4AA', '#F59E0B', '#EF4444']
      });
      setTimeout(() => {
        navigate('/dashboard');
      }, 2500);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden" 
         style={{ background: '#0D0D1A', padding: '40px 20px' }}>
      
      {/* Background elements */}
      <div style={{ position: 'absolute', top: '-10%', left: '-10%', width: '40vw', height: '40vw', background: 'radial-gradient(circle, rgba(108,99,255,0.15) 0%, rgba(13,13,26,0) 70%)', zIndex: 0 }} />
      <div style={{ position: 'absolute', bottom: '-20%', right: '-10%', width: '60vw', height: '60vw', background: 'radial-gradient(circle, rgba(0,212,170,0.1) 0%, rgba(13,13,26,0) 70%)', zIndex: 0 }} />

      <div style={{
        position: 'relative', zIndex: 1, width: '100%', maxWidth: 440, padding: 40,
        background: 'rgba(19, 19, 30, 0.7)', backdropFilter: 'blur(20px)',
        border: '1px solid rgba(108, 99, 255, 0.2)', borderRadius: 24,
        boxShadow: '0 20px 40px rgba(0,0,0,0.4)',
        animation: shake ? 'shake 0.5s cubic-bezier(.36,.07,.19,.97) both' : 'fadeInUp 0.6s ease-out'
      }}>
        
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <h1 style={{ fontSize: 32, fontWeight: 800, color: '#fff', margin: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
            Créer un compte
          </h1>
          <p style={{ color: '#8888AA', marginTop: 8, fontSize: 14 }}>Rejoignez AutoIntel et obtenez 100 AutoCoins !</p>
        </div>

        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #EF4444', color: '#FCA5A5', padding: '12px 16px', borderRadius: 12, marginBottom: 24, fontSize: 13, display: 'flex', alignItems: 'center', gap: 10 }}>
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        {successMsg && (
          <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10B981', color: '#6EE7B7', padding: '12px 16px', borderRadius: 12, marginBottom: 24, fontSize: 14, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 10, animation: 'fadeInUp 0.3s ease-out' }}>
            <CheckCircle2 size={18} />
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          
          <div>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#F0F0F5', marginBottom: 8 }}>Nom d'utilisateur</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#55557A' }}><User size={18} /></div>
              <input
                type="text"
                name="username"
                required
                value={formData.username}
                onChange={handleChange}
                placeholder="jean_dupont"
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
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#F0F0F5', marginBottom: 8 }}>Adresse email</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#55557A' }}><Mail size={18} /></div>
              <input
                type="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                placeholder="jean@email.com"
                style={{
                  width: '100%', padding: '14px 44px 14px 44px', borderRadius: 12,
                  background: 'rgba(0,0,0,0.2)', border: '1px solid #2a2a3e', color: '#fff', fontSize: 15,
                  outline: 'none', transition: 'all 0.2s'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6C63FF'}
                onBlur={(e) => e.target.style.borderColor = '#2a2a3e'}
              />
              {isEmailValid && <div style={{ position: 'absolute', right: 14, top: '50%', transform: 'translateY(-50%)', color: '#10B981' }}><CheckCircle2 size={18} /></div>}
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#F0F0F5', marginBottom: 8 }}>Mot de passe</label>
            <div style={{ position: 'relative', marginBottom: 6 }}>
              <div style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#55557A' }}><Lock size={18} /></div>
              <input
                type="password"
                name="password"
                required
                value={formData.password}
                onChange={handleChange}
                placeholder="Min 8 caractères"
                style={{
                  width: '100%', padding: '14px 14px 14px 44px', borderRadius: 12,
                  background: 'rgba(0,0,0,0.2)', border: '1px solid #2a2a3e', color: '#fff', fontSize: 15,
                  outline: 'none', transition: 'all 0.2s'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6C63FF'}
                onBlur={(e) => e.target.style.borderColor = '#2a2a3e'}
              />
            </div>
            {/* Password strength bar */}
            <div style={{ height: 4, borderRadius: 2, background: '#2a2a3e', width: '100%', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: passStrength === 0 ? '0%' : passStrength === 1 ? '33%' : passStrength === 2 ? '66%' : '100%', background: strengthColor, transition: 'all 0.3s ease' }} />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#F0F0F5', marginBottom: 8 }}>Confirmer le mot de passe</label>
            <div style={{ position: 'relative' }}>
              <div style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#55557A' }}><Lock size={18} /></div>
              <input
                type="password"
                name="password_confirm"
                required
                value={formData.password_confirm}
                onChange={handleChange}
                placeholder="••••••••"
                style={{
                  width: '100%', padding: '14px 44px 14px 44px', borderRadius: 12,
                  background: 'rgba(0,0,0,0.2)', border: '1px solid #2a2a3e', color: '#fff', fontSize: 15,
                  outline: 'none', transition: 'all 0.2s'
                }}
                onFocus={(e) => e.target.style.borderColor = '#6C63FF'}
                onBlur={(e) => e.target.style.borderColor = '#2a2a3e'}
              />
              {formData.password_confirm.length > 0 && isPassMatch && <div style={{ position: 'absolute', right: 14, top: '50%', transform: 'translateY(-50%)', color: '#10B981' }}><CheckCircle2 size={18} /></div>}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !isValid}
            style={{
              padding: '16px', borderRadius: 12, border: 'none', cursor: (loading || !isValid) ? 'not-allowed' : 'pointer',
              background: (loading || !isValid) ? '#3f3f5a' : 'linear-gradient(135deg, #6C63FF, #9B59B6)', color: (loading || !isValid) ? '#888' : '#fff', fontWeight: 700, fontSize: 15,
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
              boxShadow: (loading || !isValid) ? 'none' : '0 8px 24px rgba(108, 99, 255, 0.3)', transition: 'all 0.2s', marginTop: 10,
              opacity: loading ? 0.7 : 1, transform: 'scale(1)'
            }}
            onMouseEnter={(e) => { if(!loading && isValid) e.currentTarget.style.transform = 'scale(1.02)' }}
            onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)' }}
          >
            {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> : null}
            {loading ? 'Inscription...' : 'S\'inscrire'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: 32 }}>
          <p style={{ color: '#8888AA', fontSize: 13 }}>
            Déjà un compte ?{' '}
            <Link to="/login" style={{ color: '#fff', fontWeight: 600, textDecoration: 'none' }}>
              Se connecter →
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

export default Register;
