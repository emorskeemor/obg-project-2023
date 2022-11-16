import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/dashboard/HomeView.vue'
// errors
import PermissionDeniedView from '@/views/error/PermissionDeniedView.vue'
import ResourceNotFound from '@/views/error/ResourceNotFound.vue'
import ServerError from '@/views/error/ServerErrorView.vue' 
// auth
import LoginView from '@/views/auth/LoginView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'
// students and rooms
import RoomJoinView from '@/views/room/RoomJoinView.vue'
import StudentCredentialsView from '@/views/room/StudentAccessView.vue'
import ChoicesView from '@/views/room/ChoicesView.vue'
// teacher
import TeacherDashboardView from '@/views/dashboard/TeacherDashboardView.vue'

import { isLoggedIn } from 'axios-jwt'
import RoomEditView from '@/views/room/RoomEditView.vue'

// http://localhost:8080/user/352a7ee2-b55d-4096-a0c7-77a4e482f91d/dashboard

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // error webpages
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
  // authentication web pages
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
  // other related
  {
    path: '/room/join',
    name: 'room-join',
    component: RoomJoinView
  },
  {
    path: '/u/:user_id/dashboard',
    name: 'user-dashboard',
    component: TeacherDashboardView,
    beforeEnter: (to, from) => {
      if (!isLoggedIn()){
        return {name:"E404"}
      }
    },
    
  },
  {
    path: '/u/:user_id/r/:domain/:room_id/edit',
    name: 'room-edit',
    component: RoomEditView,
    beforeEnter: (to, from) => {
      if (!isLoggedIn()){
        return {name:"E404"}
      }
    },
  },
  {
    path: '/u/join/:domain/:code/verify',
    name: 'room-verification',
    component: StudentCredentialsView
  },
  {
    path: '/u/:domain/:code/s/:id',
    name: 'student-choice',
    component: ChoicesView
  },
  // 404 error as no url path matched
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
