import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/main/HomeView.vue'
// auth
import PermissionDeniedView from '@/views/error/PermissionDeniedView.vue'
import ResourceNotFound from '@/views/error/ResourceNotFound.vue'
import ServerError from '@/views/error/ServerErrorView.vue' 
import LoginView from '@/views/auth/LoginView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'
import RoomJoinView from '@/views/room/RoomJoinView.vue'
import TeacherDashboardView from '@/views/main/TeacherDashboardView.vue'

import { isLoggedIn } from 'axios-jwt'

// http://localhost:8080/user/352a7ee2-b55d-4096-a0c7-77a4e482f91d/dashboard

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
    path: '/404',
    name: 'E404',
    component: ResourceNotFound
  },
  {
    path: '/500',
    name: 'E500',
    component: ServerError
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
    path: '/room/join',
    name: 'room-join',
    component: RoomJoinView
  },
  {
    path: '/user/:user_id/dashboard',
    name: 'user-dashboard',
    component: TeacherDashboardView,
    beforeEnter: (to, from) => {
      if (!isLoggedIn()){
        return {name:"E404"}
      }
    },
    
  },
  { 
    path: "/:pathMatch(.*)*", 
    component: ResourceNotFound 
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

// {
//   path: '/room/',
//   name: 'generator',
//   component: GeneratorTestView,
//   beforeEnter: (to, from) => {return isLoggedIn()}
// },
