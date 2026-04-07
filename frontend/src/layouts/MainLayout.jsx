import { Outlet } from 'react-router-dom';
import Sidebar from '../components/ui/Sidebar';
import Navbar from '../components/ui/Navbar';

export default function MainLayout() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#0D0D14' }}>
      <Sidebar />
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        <Navbar />
        <main
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '28px 32px',
          }}
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}
