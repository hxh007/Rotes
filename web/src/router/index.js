import Vue from 'vue'
import Router from 'vue-router'
import routes from './routers'
import instance from '../../libs/axios'
import store from '@/store'

Vue.use(Router)
const router = new Router({
  routes
})
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('userToken')
  if (token && token !== 'null') { // 登录-> 查询登录用户信息
    store.dispatch('setToken', token)
    instance.get('/back/userInfo', {
      headers: {
        Authorization: 'JWT ' + token
      }
    }).then((response) => {
      const res = response.data
      if (res.code === 0) {
        store.dispatch('setUserId', res.data.user_info.id)
        store.dispatch('setUser', res.data.user_info.name)
        // store.dispatch('setToken', data.jwt_token)
        store.dispatch('setDeparts', res.data.depart_list)
        store.dispatch('setGroups', res.data.group_list)
        store.dispatch('setPermissions', res.data.permission_list)
      } else if (res.code === 2) {
        // 需要重新登录
        store.commit('setUserId', null)
        store.commit('userStatus', null)
        store.commit('setDeparts', [])
        store.commit('setPermissions', {})
        store.commit('setGroups', [])
        localStorage.setItem('userName', null)
        localStorage.setItem('userToken', null)
        switch (to.path) {
          case '/' || '/home' || '/schedule' || '/login' || '/register':
            next()
            break
          case to.path.indexOf('/backend') > -1:
            next('/')
            break
          default:
            next()
        }
      }
    })
  }
  next()
})

export default router
