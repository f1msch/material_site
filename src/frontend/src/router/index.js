import { createRouter, createWebHashHistory } from 'vue-router'
import MaterialList from '../views/MaterialList.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/materials'
  },
  {
    path: '/materials',
    name: 'MaterialList',
    component: MaterialList
  }
]

const router = createRouter({
//  history: createWebHistory(),
  history: createWebHashHistory(), // 使用hash模式
  routes
})

export default router