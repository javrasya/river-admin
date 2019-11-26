module.exports = {
      // options...
      publicPath: "/static/",
      outputDir: __dirname + '/river_admin/templates/',
      assetsDir: '../static/',
      devServer: {
            proxy: 'http://localhost:8000/',
      },

      configureWebpack: {
            resolve: {
                  alias: {
                        '@': __dirname + '/ui/src/'
                  }
            },
            entry: {
                  app: __dirname + '/ui/src/main.js'
            }
      }
}