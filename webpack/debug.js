'use strict';

var config = require('./base.js'),
    ExtractText = require('extract-text-webpack-plugin'),
    BundleTracker = require('webpack-bundle-tracker'),
    path = require('path'),
    base_dir = path.dirname(__dirname);

// generate source maps for js & css bundles
config.devtool = 'source-map';

config.output = {
  path: path.join(base_dir, 'assets/debug'),
  filename: '[name]-[hash].js',
  chunkFilename: '[name]-[hash].js'
};

config.plugins = config.plugins.concat([
  // split off css
  new ExtractText('[name]-[hash].css'),

  new BundleTracker({
    path: path.join(base_dir, 'webpack'),
    filename: 'stats-debug.json'
  })
]);

module.exports = config;
