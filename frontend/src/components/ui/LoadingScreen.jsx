import React, { useState, useEffect } from 'react';

export default function LoadingScreen() {
  const messages = ["Analyse du marché...", "Connexion sécurisée...", "Chargement des données...", "Prêt !"];
  const [msgIndex, setMsgIndex] = useState(0);
  const [fading, setFading] = useState(false);

  useEffect(() => {
    let interval;
    if (msgIndex < messages.length - 1) {
      interval = setInterval(() => {
        setMsgIndex(prev => prev + 1);
      }, 600);
    } else {
      setTimeout(() => setFading(true), 600);
    }
    return () => clearInterval(interval);
  }, [msgIndex, messages.length]);

  return (
    <div style={{
      position: 'fixed', inset: 0,
      background: '#0D0D14', zIndex: 9999,
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      opacity: fading ? 0 : 1, transition: 'opacity 0.4s ease',
      pointerEvents: fading ? 'none' : 'auto'
    }}>
      <div style={{ position: 'absolute', top: 0, left: 0, height: 3, background: '#6C63FF', width: `${((msgIndex + 1) / messages.length) * 100}%`, transition: 'width 0.6s ease' }} />
      <h1 className="animate-pulse" style={{ color: '#fff', fontSize: 32, fontWeight: 900, marginBottom: 16 }}>
        ⚡ AutoIntel
      </h1>
      <p style={{ color: '#8B8BA0', fontSize: 14 }}>{messages[msgIndex]}</p>
    </div>
  );
}
