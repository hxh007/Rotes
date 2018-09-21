import Vue from 'vue'
import Router from 'vue-router'
import routes from './routers'
import axios from 'axios'
import store from '@/store'
// import iView from 'iview'
// import { getToken } from '../../libs/util'
Vue.use(Router)
const router = new Router({
  routes
})
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('userToken')
  if (token) { // 登录-> 查询登录用户信息
    store.dispatch('setToken', token)
    axios.get('/back/userInfo', {
      headers: {
        Authorization: 'JWT ' + token
      }
    }).then((response) => {
      const res = response.data
      if (res.code === 0) {
        store.dispatch('setDeparts', res.data.depart_list)
        store.dispatch('setGroups', res.data.group_list)
      } else if (res.code === 2) {
        // 需要重新登录
        store.commit('userStatus', null)
        localStorage.setItem('userName', null)
        localStorage.setItem('userToken', null)
      }
    })
  } else { // 未登录

  }
  // if ((token === 'undefined' || !token) && to.name !== 'Login') {
  //   // 未登录且要跳转的页面不是登录页
  //   next({
  //     name: 'Login' // 跳转到登录页
  //   })
  // } else if ((token === 'undefined' || !token) && to.name === 'Login') {
  //   // 未登陆且要跳转的页面是登录页
  //   next() // 跳转
  // } else if (token && typeof token !== 'string' && to.name === 'Login') {
  //   // 已登录且要跳转的页面是登录页
  //   next({
  //     name: 'Login' // 跳转到login页
  //   })
  // } else { // 已登录且跳转的不是登录页
  //   next()
  // }
  next()
})

export default router
