/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // path to all app templates
    // '**/templates/**/*.html',
    // '**/templates/**/**/*.html',
    // '**/static/**/*.js',
    // Posle za build
    './shop/templates/**/*.html',
    './shop/templates/**/**/*.html',
    './shop/templates/**/**/**/*.html',

  ],
  theme: {
    extend: {
      animation: {
        'spinner': 'spinner 0.75s infinite linear',
      },
      keyframes: {
        spinner: {
          '100%': {transform: 'rotate(360deg)'},
        },
      },
      colors: {
        'dashboard-blue': '#4759E4',
        'dashboard-item-active': '#95A1FF',
        'dashboard-gray': '#F8FAFF',
        'brand-gray': '#9D9A99',
        'error': '#FF0000',
        'brand-primary': '#163C45',
        'brand-secondary': '#D9D9D9',
        'brand-action': '#FF4C15',
        'brand-accent': '#75FFCE',
      },
      gridTemplateColumns: {
        'dashboard-template': '300px 1fr',
      },
      gridTemplateRows: {
        'dashboard-mobile-template': 'auto 1fr',
      },

    },

    fontFamily: {
      'montserrat': ['Montserrat', 'sans-serif'],
      'mulish': ['Mulish', 'sans-serif'],
      'century-gothic': ['"Century Gothic Paneuropean"', 'Arial', 'sans-serif'],
    },


  },
  plugins: [],
};

