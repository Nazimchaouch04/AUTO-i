import { useEffect } from 'react';

const PAGE_TITLES = {
  '/':            'AutoIntel — Analyse intelligente du marché automobile',
  '/dashboard':   'Dashboard | AutoIntel',
  '/annonces':    'Annonces | AutoIntel',
  '/estimation':  'Estimation ML | AutoIntel',
  '/alertes':     'Mes alertes | AutoIntel',
  '/statistiques':'Statistiques | AutoIntel',
  '/pricing':     'Pricing & Abonnement | AutoIntel',
  '/profil':      'Mon profil | AutoIntel',
  '/abonnement':  'Abonnement | AutoIntel',
  '/shop':        'Boutique | AutoIntel',
  '/battles':     'Battles 1v1 | AutoIntel',
  '/compare':     'Comparateur | AutoIntel',
};

export function usePageTitle(path) {
  useEffect(() => {
    // Handling dynamic IDs for detail pages
    if (path.startsWith('/annonce/')) {
        document.title = 'Détail Annonce | AutoIntel';
        return;
    }
    if (path.startsWith('/battle/')) {
        document.title = 'Battle en cours | AutoIntel';
        return;
    }

    const title = PAGE_TITLES[path] || 'AutoIntel';
    document.title = title;
  }, [path]);
}
