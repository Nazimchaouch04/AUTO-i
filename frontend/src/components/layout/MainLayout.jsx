import React from 'react';
import { useLocation } from 'react-router-dom';
import { usePageTitle } from '../../hooks/usePageTitle';
import Header from '../ui/Header';
import AIFloatingButton from '../ai/AIFloatingButton';

export default function MainLayout({ children, darkMode, setDarkMode }) {
  const location = useLocation();
  usePageTitle(location.pathname);

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-primary' : 'bg-gray-50'}`}>
      <Header darkMode={darkMode} setDarkMode={setDarkMode} />
      {children}
      <AIFloatingButton />
    </div>
  );
}
