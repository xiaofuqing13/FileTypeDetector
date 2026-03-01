const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080', // 后端服务器地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': '' // 如果后端接口不是以 /api 开头，可以通过这个设置来重写路径
        }
      }
    }
  }
}