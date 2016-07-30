'use strict';

var config = require('./base.js'),
    webpack = require('webpack'),
    ExtractText = require('extract-text-webpack-plugin'),
    BundleTracker = require('webpack-bundle-tracker'),
    path = require('path'),
    base_dir = path.dirname(__dirname);

config.output = {
  path: path.join(base_dir, 'assets/prod'),
  filename: '[name].js',
  chunkFilename: '[name].js'
};

config.plugins = config.plugins.concat([
  // aggressively remove duplicate modules
  new webpack.optimize.DedupePlugin(),

  // remove a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
    }
  }),

  // keep hashes consistent between compilations
  new webpack.optimize.OccurenceOrderPlugin(),

  // minify code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  }),

  // split off css
  new ExtractText('[name].css'),

  new BundleTracker({
    path: path.join(base_dir, 'webpack'),
    filename: 'stats-prod.json'
  })
]);

module.exports = config;
