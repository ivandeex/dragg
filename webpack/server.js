'use strict';

var config = require('./debug.js'),
    webpack = require('webpack'),
    WebpackDevServer = require('webpack-dev-server'),
    dev_host = process.env.DEV_HOST || 'localhost',
    dev_port = process.env.DEV_PORT || 3000;

config.entry.unshift(`webpack-dev-server/client?http://${dev_host}:${dev_port}`);

// Let Django load packages from this URL instead of STATIC_URL + bundle_name
config.output.publicPath = `http://${dev_host}:${dev_port}/assets/debug/`;

var server = new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath
});

server.listen(dev_port, '0.0.0.0', function(err, result) {
  if (err)  console.log(err);
  console.log(`Listening on ${dev_host}:${dev_port}`);
});
