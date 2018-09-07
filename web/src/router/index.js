import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/components/Layout'
import Home from '@/pages/home/Home'
import Schedule from '@/pages/schedule/Schedule'
import UserManage from '@/pages/backend/UserManage'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Layout',
      component: Layout,
      redirect: '/home',
      children: [{
        path: '/home',
        name: 'Home',
        component: Home
      }, {
        path: '/schedule',
        name: 'Schedule',
        component: Schedule
      }]
    }, {
      path: '/backend',
      name: 'Backend',
      component: Layout,
      redirect: '/backend/userManage',
      children: [{
        path: '/backend/userManage',
        name: 'UserManage',
        component: UserManage
      }]
    }
  ]
})
