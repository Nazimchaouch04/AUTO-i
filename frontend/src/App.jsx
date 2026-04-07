import { BrowserRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Suspense, lazy } from 'react';

// Layouts
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';

// Public
const LandingPage = lazy(() => import('./pages/LandingPage'));

// Auth
const LoginPage = lazy(() => import('./pages/auth/LoginPage'));
const RegisterPage = lazy(() => import('./pages/auth/RegisterPage'));

// Core pages
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const AnnoncesPage = lazy(() => import('./pages/AnnoncesPage'));
const EstimationPage = lazy(() => import('./pages/EstimationPage'));
const AlertesPage = lazy(() => import('./pages/AlertesPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));
const AbonnementPage = lazy(() => import('./pages/AbonnementPage'));

// Gamification pages
const ClassementPage = lazy(() => import('./pages/gamification/ClassementPage'));
const DefisPage = lazy(() => import('./pages/gamification/DefisPage'));
const BoutiquePage = lazy(() => import('./pages/gamification/BoutiquePage'));
const BattlesPage = lazy(() => import('./pages/gamification/BattlesPage'));
const TournoisPage = lazy(() => import('./pages/gamification/TournoisPage'));
const CollectionPage = lazy(() => import('./pages/gamification/CollectionPage'));
const SeasonPassPage = lazy(() => import('./pages/gamification/SeasonPassPage'));

function PageLoader() {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#0D0D14',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#6C63FF',
        fontSize: 16,
        gap: 12,
      }}
    >
      <span
        style={{
          width: 20,
          height: 20,
          border: '2px solid #6C63FF',
          borderTopColor: 'transparent',
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite',
          display: 'inline-block',
        }}
      />
      Chargement...
      <style>{'@keyframes spin { to { transform: rotate(360deg); } }'}</style>
    </div>
  );
}

function PrivateRoute({ children }) {
  const { isAuthenticated } = useSelector((s) => s.user);
  const location = useLocation();
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}

function NotFound() {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#0D0D14',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#F0F0F5',
        gap: 16,
      }}
    >
      <div style={{ fontSize: 64 }}>🚗</div>
      <h1 style={{ fontSize: 24, fontWeight: 500 }}>Page introuvable</h1>
      <a
        href="/"
        style={{
          color: '#6C63FF',
          textDecoration: 'none',
          fontSize: 14,
        }}
      >
        ← Retour a l'accueil
      </a>
    </div>
  );
}

export default function App() {
  const { isAuthenticated } = useSelector((s) => s.user);

  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* Public landing */}
          <Route
            path="/"
            element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LandingPage />}
          />

          {/* Auth */}
          <Route element={<AuthLayout />}>
            <Route
              path="/login"
              element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />}
            />
            <Route
              path="/register"
              element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />}
            />
          </Route>

          {/* Protected area */}
          <Route
            element={(
              <PrivateRoute>
                <MainLayout />
              </PrivateRoute>
            )}
          >
            {/* Core */}
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/annonces" element={<AnnoncesPage />} />
            <Route path="/estimation" element={<EstimationPage />} />
            <Route path="/alertes" element={<AlertesPage />} />
            <Route path="/profil" element={<ProfilePage />} />
            <Route path="/abonnement" element={<AbonnementPage />} />

            {/* Gamification */}
            <Route path="/classement" element={<ClassementPage />} />
            <Route path="/defis" element={<DefisPage />} />
            <Route path="/boutique" element={<BoutiquePage />} />
            <Route path="/battles" element={<BattlesPage />} />
            <Route path="/tournois" element={<TournoisPage />} />
            <Route path="/collection" element={<CollectionPage />} />
            <Route path="/season-pass" element={<SeasonPassPage />} />
          </Route>

          {/* 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
