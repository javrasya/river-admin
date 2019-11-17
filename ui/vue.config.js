module.exports = {
      // options...
      outputDir: '../backend/river_admin/templates/',
      assetsDir: '../static/',
      devServer: {
            proxy: 'http://localhost:8000/',
      }
}