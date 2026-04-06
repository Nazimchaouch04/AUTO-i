import { createContext, useContext, useState, useCallback } from 'react';

const ToastContext = createContext(null);

const TOAST_STYLES = {
  success: { bg: 'rgba(0,212,170,0.12)', border: '#00D4AA30', color: '#00D4AA', icon: '✓' },
  error:   { bg: 'rgba(239,68,68,0.12)', border: '#EF444430', color: '#EF4444', icon: '✗' },
  info:    { bg: 'rgba(108,99,255,0.12)', border: '#6C63FF30', color: '#6C63FF', icon: 'ℹ' },
  coin:    { bg: 'rgba(245,158,11,0.12)', border: '#F59E0B30', color: '#F59E0B', icon: '🪙' },
  levelup: { bg: 'rgba(108,99,255,0.2)',  border: '#6C63FF50', color: '#A78BFA', icon: '⬆' },
};

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback(({ message, type = 'info', duration = 3000 }) => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, duration);
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div style={{
        position: 'fixed', bottom: 24, right: 24,
        zIndex: 9999, display: 'flex', flexDirection: 'column', gap: 8,
      }}>
        {toasts.map(toast => {
          const s = TOAST_STYLES[toast.type] || TOAST_STYLES.info;
          return (
            <div key={toast.id} style={{
              background: s.bg,
              border: `1px solid ${s.border}`,
              borderRadius: 10, padding: '12px 16px',
              display: 'flex', alignItems: 'center', gap: 10,
              minWidth: 260, maxWidth: 340,
              animation: 'slideInRight 0.3s ease',
              backdropFilter: 'blur(8px)',
            }}>
              <span style={{ color: s.color, fontSize: 16 }}>{s.icon}</span>
              <span style={{ color: '#F0F0F5', fontSize: 13 }}>{toast.message}</span>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);
