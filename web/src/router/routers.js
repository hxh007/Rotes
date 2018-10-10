import Layout from '@/components/Layout'
import Home from '@/pages/home/Home'
import Schedule from '@/pages/schedule/Schedule'
import UserManage from '@/pages/backend/UserManage'
import AdminManage from '@/pages/backend/AdminManage'
import DepartManage from '@/pages/backend/DepartManage'
import RoleManage from '@/pages/backend/RoleManage'
import OperationManage from '@/pages/backend/OperationManage'
import PermissionManage from '@/pages/backend/PermissionManage'
import MessageManage from '@/pages/backend/MessageManage'
import PlanTaskManage from '@/pages/backend/PlanTaskManage'
import Login from '@/pages/login/Login'
import oauthCB from '@/pages/login/oauth_callback'
import Register from '@/pages/register/Register'
export default [
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
    redirect: '/userManage',
    children: [{
      path: '/userManage',
      name: 'UserManage',
      component: UserManage
    }, {
      path: '/permissionManage',
      name: 'PermissionManage',
      component: PermissionManage
    }, {
      path: '/departManage',
      name: 'DepartManage',
      component: DepartManage
    }, {
      path: '/roleManage',
      name: 'RoleManage',
      component: RoleManage
    }, {
      path: '/adminManage',
      name: 'AdminManage',
      component: AdminManage
    }, {
      path: '/operationManage',
      name: 'OperationManage',
      component: OperationManage
    }, {
      path: '/messageManage',
      name: 'messageManage',
      component: MessageManage
    }, {
      path: '/planTaskManage',
      name: 'planTaskManage',
      component: PlanTaskManage
    }]
  }, {
    path: '/login',
    name: 'Login',
    component: Login
  }, {
    path: '/register',
    name: 'Register',
    component: Register
  }, {
    path: '/oauth_callback',
    name: 'oauth_callback',
    component: oauthCB
  }
  // { path: '*', component: NotFoundComponent }
]
