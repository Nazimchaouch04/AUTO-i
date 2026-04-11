// Script de test pour vérifier toutes les routes de l'application
const routes = [
  // Routes publiques
  '/',
  '/login',
  '/register',
  
  // Routes protégées (nécessitent authentification)
  '/dashboard',
  '/annonces',
  '/estimation',
  '/alertes',
  '/profil',
  '/abonnement',
  
  // Gamification
  '/classement',
  '/defis',
  '/boutique',
  '/battles',
  '/tournois',
  '/collection',
  '/season-pass'
];

console.log('Routes à tester dans le navigateur:');
routes.forEach((route, index) => {
  console.log(`${index + 1}. http://localhost:5174${route}`);
});

console.log('\nInstructions:');
console.log('1. Ouvrez chaque URL dans le navigateur');
console.log('2. Vérifiez que la page se charge sans erreur 404');
console.log('3. Pour les routes protégées, vous serez redirigé vers /login si non authentifié');
console.log('4. Vérifiez que les composants se rendent correctement');
