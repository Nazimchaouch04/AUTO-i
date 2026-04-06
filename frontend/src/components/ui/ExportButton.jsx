import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

export default function ExportButton({ endpoint, filename, label = 'Exporter CSV' }) {
  const [loading, setLoading] = useState(false);
  const { user } = useSelector(s => s.user);
  const navigate = useNavigate();
  // We check if plan is pro or business
  const isPro = ['pro', 'business'].includes(user?.plan_nom);

  const handleExport = async () => {
    if (!isPro) {
      navigate('/pricing');
      return;
    }
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error("Erreur export");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={loading}
      className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all border whitespace-nowrap ${isPro ? 'bg-primary-elevated text-primary-text-secondary border-primary-border/DEFAULT hover:text-white' : 'bg-warning/10 border-warning/30 text-warning hover:bg-warning/20'}`}
    >
      {loading ? <span className="animate-pulse">...</span> : '📥'}
      {isPro ? label : `${label} (Pro)`}
    </button>
  );
}
