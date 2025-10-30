import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Bootstrap配置
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

// Axios配置
import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(VueAxios, axios)

// 配置axios基础URL
axios.defaults.baseURL = 'http://localhost:8000'

app.mount('#app')