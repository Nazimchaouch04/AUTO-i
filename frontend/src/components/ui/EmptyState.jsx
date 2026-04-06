export default function EmptyState({ icon, title, subtitle, actionLabel, onAction }) {
  return (
    <div style={{
      textAlign: 'center', padding: '80px 20px',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', gap: 12,
    }}>
      <div style={{ fontSize: 56, filter: 'grayscale(0.3)',
                    marginBottom: 8 }}>{icon}</div>
      <h3 style={{ color: '#F0F0F5', fontSize: 18,
                   fontWeight: 500, margin: 0 }}>{title}</h3>
      <p style={{ color: '#8B8BA0', fontSize: 14,
                  maxWidth: 300, margin: 0 }}>{subtitle}</p>
      {actionLabel && (
        <button onClick={onAction} style={{
          marginTop: 8, background: '#6C63FF', color: '#fff',
          border: 'none', borderRadius: 8, padding: '10px 20px',
          fontSize: 14, fontWeight: 500, cursor: 'pointer',
        }}>
          {actionLabel}
        </button>
      )}
    </div>
  );
}
