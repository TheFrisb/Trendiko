/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // path to all app templates
    // '**/templates/**/*.html',
    // '**/templates/**/**/*.html',
    // '**/static/**/*.js',
    'shop/templates/**/*.html',
    'shop/templates/**/**/*.html',
    'shop/static/**/*.js',

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
        'brand-gray': '#F8FAFF',
        'error': '#FF0000',
        'brand-yellow': '#F0DA1F',
        'brand-primary': '#21872f',
        'brand-secondary': '#17335E',
        'brand-tertiary': '#53175E',
      },
      gridTemplateColumns: {
        'dashboard-template': '300px 1fr',
      },
      gridTemplateRows: {
        'dashboard-mobile-template': 'auto 1fr',
      },
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

