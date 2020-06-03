const path = require('path');
const PnpWebpackPlugin = require('pnp-webpack-plugin');

module.exports = {
    entry: {
        app: './src/js/main.js'
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].bundle.js'
    },
    resolve: {
        alias: {
            js: path.resolve(__dirname, 'src/js'),
            css: path.resolve(__dirname, 'src/css')
        },
        plugins: [
            PnpWebpackPlugin,
        ]
    },
    resolveLoader: {
        plugins: [
            PnpWebpackPlugin.moduleLoader(module)
        ]
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader'
                ],
            }
        ]
    }
};