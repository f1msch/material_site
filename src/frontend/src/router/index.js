import { createRouter, createWebHashHistory } from 'vue-router'
import MaterialManager from '../views/MaterialManager.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/materials'
  },
  {
    path: '/materials',
    name: 'MaterialList',
    component: MaterialManager
  }
]

const router = createRouter({
//  history: createWebHistory(),
  history: createWebHashHistory(), // 使用hash模式
  routes
})

export default router