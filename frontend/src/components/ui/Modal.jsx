import { useEffect } from 'react';

export default function Modal({ isOpen, onClose, title, children, size = 'medium' }) {
  useEffect(() => {
    const handleEsc = (e) => { if (e.key === 'Escape') onClose(); };
    if (isOpen) document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sizes = { small: 400, medium: 560, large: 760 };

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed', inset: 0,
        background: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(4px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 1000,
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          background: '#13131E',
          border: '1px solid rgba(255,255,255,0.1)',
          borderRadius: 16, padding: 28,
          width: '90%', maxWidth: sizes[size],
          maxHeight: '85vh', overflowY: 'auto',
          animation: 'scaleIn 0.2s ease',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between',
                      alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ color: '#F0F0F5', fontSize: 16,
                       fontWeight: 500, margin: 0 }}>{title}</h2>
          <button onClick={onClose} style={{
            background: 'none', border: 'none',
            color: '#8B8BA0', cursor: 'pointer', fontSize: 20,
          }}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
}
