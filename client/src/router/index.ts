import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/misc/HomeView.vue'
// auth
import PermissionDeniedView from '@/views/error/PermissionDeniedView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'

import { isLoggedIn } from 'axios-jwt'

import GeneratorTestView from '@/views/gen/GeneratorTestView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/401',
    name: 'E401',
    component: PermissionDeniedView
  },
  {
    path: '/auth/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/auth/logout',
    name: 'logout',
    component: LogoutView
  },
  {
    path: '/generator',
    name: 'generator',
    component: GeneratorTestView,
    beforeEnter: (to, from) => {return isLoggedIn()}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
