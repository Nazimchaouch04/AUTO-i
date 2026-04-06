import Modal from './Modal';

export default function ConfirmDialog({ isOpen, onClose, onConfirm,
  title, message, confirmLabel = 'Confirmer', danger = false }) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title} size="small">
      <p style={{ color: '#8B8BA0', fontSize: 14,
                  marginBottom: 24 }}>{message}</p>
      <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
        <button onClick={onClose} style={{
          background: 'transparent', border: '1px solid rgba(255,255,255,0.1)',
          color: '#8B8BA0', borderRadius: 8, padding: '8px 16px',
          cursor: 'pointer', fontSize: 13,
        }}>
          Annuler
        </button>
        <button onClick={() => { onConfirm(); onClose(); }} style={{
          background: danger ? '#EF4444' : '#6C63FF',
          color: '#fff', border: 'none', borderRadius: 8,
          padding: '8px 16px', cursor: 'pointer', fontSize: 13, fontWeight: 500,
        }}>
          {confirmLabel}
        </button>
      </div>
    </Modal>
  );
}
