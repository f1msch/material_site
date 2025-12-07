import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'
import {useUserStore} from '@/stores/user'
import type {RouteMetaCustom} from '@/types'

declare module 'vue-router' {
    interface RouteMeta extends RouteMetaCustom {
    }
}

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: {
            title: '首页'
        }
    },
    {
        path: '/materials',
        name: 'Materials',
        component: () => import('@/views/MaterialList.vue'),
        meta: {
            title: '素材列表'
        }
    },
    {
        path: '/materials/:id',
        name: 'MaterialDetail',
        component: () => import('@/views/MaterialDetail.vue'),
        meta: {
            title: '素材详情'
        }
    },
    {
        path: '/upload',
        name: 'Upload',
        component: () => import('@/views/Upload.vue'),
        meta: {
            requiresAuth: true,
            title: '上传素材'
        }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue'),
        meta: {
            requiresAuth: true,
            title: '个人中心'
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
        meta: {
            title: '登录'
        }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/Register.vue'),
        meta: {
            title: '注册'
        }
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/NotFound.vue'),
        meta: {
            title: '页面未找到'
        }
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
    const userStore = useUserStore()

    // 设置页面标题
    if (to.meta.title) {
        document.title = `${to.meta.title} - 素材网站`
    }

    // 检查是否需要认证
    if (to.meta.requiresAuth && !userStore.isAuthenticated) {
        // 保存原始路径，登录后跳转回来
        next({
            path: '/login',
            query: {redirect: to.fullPath}
        })
    } else {
        next()
    }
})

// 全局后置钩子
router.afterEach((to, from) => {
    // 可以在这里添加页面加载完成后的逻辑，比如统计页面访问
    console.log(`导航到: ${to.path}`)
})

export default router