import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    server: {
        port: 3001,  // 改为 3001 或其他可用端口
        host: '0.0.0.0',  // 允许所有主机访问
        // proxy: {
        //   '/api': {
        //     target: 'http://localhost:8000',
        //     changeOrigin: true
        //   },
        //   '/media': {
        //     target: 'http://localhost:8000',
        //     changeOrigin: true
        //   }
        // }
    }
})
