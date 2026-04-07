import { Outlet } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#0D0D14',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div style={{ position: 'absolute', top: 24, left: 32 }}>
        <span style={{ color: '#6C63FF', fontWeight: 700, fontSize: 20 }}>
          ⚡ AutoIntel
        </span>
      </div>
      <Outlet />
    </div>
  );
}
