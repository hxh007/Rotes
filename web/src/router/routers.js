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
    redirect: '/backend/userManage',
    children: [{
      path: '/backend/userManage',
      name: 'UserManage',
      component: UserManage
    }, {
      path: '/backend/permissionManage',
      name: 'PermissionManage',
      component: PermissionManage
    }, {
      path: '/backend/departManage',
      name: 'DepartManage',
      component: DepartManage
    }, {
      path: '/backend/roleManage',
      name: 'RoleManage',
      component: RoleManage
    }, {
      path: '/backend/adminManage',
      name: 'AdminManage',
      component: AdminManage
    }, {
      path: '/backend/operationManage',
      name: 'OperationManage',
      component: OperationManage
    }, {
      path: '/backend/messageManage',
      name: 'messageManage',
      component: MessageManage
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
]
