/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          bg: '#0D0D14',
          card: '#13131E',
          elevated: '#1C1C2E',
          accent: '#6C63FF',
          'accent-secondary': '#00D4AA',
          text: {
            primary: '#F0F0F5',
            secondary: '#8B8BA0'
          }
        },
        success: '#00D4AA',
        warning: '#F59E0B',
        danger: '#EF4444',
        border: {
          DEFAULT: 'rgba(255, 255, 255, 0.06)',
          accent: 'rgba(108, 99, 255, 0.2)'
        }
      },
      animation: {
        'shimmer': 'shimmer 1.5s infinite linear',
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in',
        'slide-up': 'slideUp 0.3s ease-out'
      },
      boxShadow: {
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 8px 16px -4px rgba(108, 99, 255, 0.15), 0 4px 8px -4px rgba(108, 99, 255, 0.1)',
        'accent': '0 4px 12px rgba(108, 99, 255, 0.25)'
      }
    }
  },
  plugins: [],
}
