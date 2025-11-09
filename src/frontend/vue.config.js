const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  // 配置 ESLint
  lintOnSave: process.env.NODE_ENV !== 'production',
  configureWebpack: {
    // 配置 Vue 3 的编译器宏
    module: {
      rules: [
        {
          test: /\.vue$/,
          loader: 'vue-loader'
        }
      ]
    }
  }
})