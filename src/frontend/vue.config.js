const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: '../backend/static/frontend',
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/frontend/'
    : '/',  // 开发环境使用根路径
  indexPath: '../../backend/templates/frontend/index.html',

  devServer: {
    port: 8080,
    historyApiFallback: true,  // 添加这个重要配置
    proxy: {
      '^/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/static': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})