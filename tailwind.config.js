/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // path to all app templates
    '**/templates/**/*.html',
    '**/templates/**/**/*.html',
    '**/templates/**/*.js',

  ],
  theme: {
    extend: {
      colors: {
        'dashboard-blue': "#4759E4",
        'dashboard-item-active': "#95A1FF",
        'dashboard-gray': "#F8FAFF",
        'brand-gray': "#F8FAFF",
        'error': '#FF0000',
        'brand-yellow': "#F0DA1F",
        'brand-primary': "#21872f",
        'brand-secondary': "#17335E",
        'brand-tertiary': "#53175E"
      },
      gridTemplateColumns: {
        'dashboard-template': '300px 1fr',
        'checkout-template': '57% 43%',
        'checkout-template-3': 'minmax(0, 1fr) minmax(0, 61rem) minmax(0, 1fr)',
        'checkout-template-4': 'minmax(0, 1fr) minmax(0, 65rem) minmax(0, 45.5rem) minmax(0, 1fr)',
        'checkout-template-1': 'minmax(0, 1fr)',
      },
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif']
      }
    },
  },
  plugins: [],
}

