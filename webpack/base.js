'use strict';

var webpack = require('webpack'),
    ExtractText = require('extract-text-webpack-plugin'),
    SplitByPath = require('webpack-split-by-path'),
    path = require('path'),
    base_dir = path.dirname(__dirname) + '/';

module.exports = {
    entry: [
      path.join(base_dir, 'project/assets/app.js')
    ],

    module: {
      loaders: [
        {
          test: /\.js$/,
          loaders: [ 'babel' ],
          exclude: /node_modules/
        },
        {
          test: /\.css$/,
          loader: ExtractText.extract('style?sourceMap', 'css?sourceMap')
        },
        {
          test: /\.scss$/,
          loader: ExtractText.extract('style?sourceMap', 'css?sourceMap!sass?sourceMap')
        },
        {
          test: /\.(png|jpg|svg|woff|woff2|eot|ttf)$/,
          loader: 'url?limit=10000&name=[name].[ext]'
        }
      ]
    },

    sassLoader: {
      includePaths: [
        base_dir
      ]
    },

    plugins: [
      // don't publish if compilation fails
      new webpack.NoErrorsPlugin(),

      // split off vendor bundle
      new SplitByPath([
        { name: 'vendor', path: path.join(base_dir, 'node_modules') }
      ])
    ]
};
