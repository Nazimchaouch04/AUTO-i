// Formatage des devises
export const formatCurrency = (amount, currency = 'EUR') => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency,
  }).format(amount);
};

// Formatage des nombres avec séparateurs
export const formatNumber = (number) => {
  return new Intl.NumberFormat('fr-FR').format(number);
};

// Formatage des kilomètres
export const formatKilometers = (km) => {
  return `${formatNumber(km)} km`;
};

// Formatage des dates
export const formatDate = (date, options = {}) => {
  const defaultOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options,
  };
  return new Date(date).toLocaleDateString('fr-FR', defaultOptions);
};

// Formatage des dates relatives
export const formatRelativeTime = (date) => {
  const now = new Date();
  const targetDate = new Date(date);
  const diffInSeconds = Math.floor((now - targetDate) / 1000);

  if (diffInSeconds < 60) return 'à l\'instant';
  if (diffInSeconds < 3600) return `il y a ${Math.floor(diffInSeconds / 60)} min`;
  if (diffInSeconds < 86400) return `il y a ${Math.floor(diffInSeconds / 3600)} h`;
  if (diffInSeconds < 604800) return `il y a ${Math.floor(diffInSeconds / 86400)} j`;
  
  return formatDate(date);
};

// Formatage des pourcentages
export const formatPercentage = (value, decimals = 1) => {
  return `${(value * 100).toFixed(decimals)}%`;
};

// Validation et formatage des téléphones
export const formatPhoneNumber = (phone) => {
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return cleaned.replace(/(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/, '$1 $2 $3 $4 $5');
  }
  return phone;
};

// Tronquer le texte avec ellipsis
export const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

// Capitaliser la première lettre
export const capitalize = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

// Formatage des noms de fichiers
export const formatFileName = (name) => {
  return name.toLowerCase().replace(/[^a-z0-9.]/g, '-');
};
