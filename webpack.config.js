const path = require('path');

module.exports = {
  entry: {
    'shop': './src/shop/index.js',  // Entry point for the shop app
    'shop_manager': './src/shop_manager/index.js',  // Entry point for the shop_manager app
  },
  output: {
    path: path.resolve(__dirname, 'static/bundles'),  // Output directory
    filename: '[name]_v3.bundle.js',  // Output bundle name, based on the entry point key
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],  // Use Babel to transpile ES6+ to compatible JavaScript
          }
        }
      }
    ]
  }
};
