import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '广场 - Vestige' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录 - Vestige' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册 - Vestige' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '仪表盘 - Vestige', requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard/articles'
      },
      {
        path: 'articles',
        name: 'DashboardArticles',
        component: () => import('@/views/DashboardArticles.vue'),
        meta: { title: '文章管理 - Vestige', requiresAuth: true }
      },
      {
        path: 'articles/new',
        name: 'ArticleNew',
        component: () => import('@/views/ArticleEditor.vue'),
        meta: { title: '新建文章 - Vestige', requiresAuth: true }
      },
      {
        path: 'articles/:id',
        name: 'ArticleEdit',
        component: () => import('@/views/ArticleEditor.vue'),
        meta: { title: '编辑文章 - Vestige', requiresAuth: true }
      },
      {
        path: 'projects',
        name: 'DashboardProjects',
        component: () => import('@/views/DashboardProjects.vue'),
        meta: { title: '作品管理 - Vestige', requiresAuth: true }
      },
      {
        path: 'projects/new',
        name: 'ProjectNew',
        component: () => import('@/views/ProjectEditor.vue'),
        meta: { title: '新建作品 - Vestige', requiresAuth: true }
      },
      {
        path: 'projects/:id',
        name: 'ProjectEdit',
        component: () => import('@/views/ProjectEditor.vue'),
        meta: { title: '编辑作品 - Vestige', requiresAuth: true }
      },
      {
        path: 'keys',
        name: 'ApiKeys',
        component: () => import('@/views/ApiKeys.vue'),
        meta: { title: 'API Keys - Vestige', requiresAuth: true }
      },
      {
        path: 'favorites',
        name: 'Favorites',
        component: () => import('@/views/DashboardFavorites.vue'),
        meta: { title: '我的收藏 - Vestige', requiresAuth: true }
      },
      {
        path: 'follows',
        name: 'Follows',
        component: () => import('@/views/FollowPage.vue'),
        meta: { title: '关注/粉丝 - Vestige', requiresAuth: true }
      },
      {
        path: 'subscriptions',
        name: 'SubscriptionFeed',
        component: () => import('@/views/SubscriptionFeed.vue'),
        meta: { title: '订阅推送 - Vestige', requiresAuth: true }
      },
      {
        path: 'subscriptions/manage',
        name: 'SubscriptionManage',
        component: () => import('@/views/SubscriptionManage.vue'),
        meta: { title: '管理订阅 - Vestige', requiresAuth: true }
      },
      {
        path: 'card',
        name: 'MyCard',
        component: () => import('@/views/DashboardMyCard.vue'),
        meta: { title: '我的名片 - Vestige', requiresAuth: true }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
        meta: { title: '设置 - Vestige', requiresAuth: true }
      }
    ]
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: () => import('@/views/ArticleDetail.vue'),
    meta: { title: '文章详情 - Vestige' }
  },
  {
    path: '/project/:id',
    name: 'ProjectDetail',
    component: () => import('@/views/ProjectDetail.vue'),
    meta: { title: '作品详情 - Vestige' }
  },
  {
    path: '/user/:id',
    name: 'UserPage',
    component: () => import('@/views/UserPage.vue'),
    meta: { title: '用户主页 - Vestige' }
  },
  {
    path: '/card/:id',
    name: 'CardPage',
    component: () => import('@/views/CardPage.vue'),
    meta: { title: '个人名片 - Vestige' }
  },
  {
    path: '/ai-api',
    name: 'AiApiDoc',
    component: () => import('@/views/AiApiDoc.vue'),
    meta: { title: 'AI API文档 - Vestige' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  // Update page title
  document.title = to.meta.title as string || 'Vestige - 古墟'
  
  // Check authentication
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router