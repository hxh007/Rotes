import instance from 'axios'
import store from '@/store'
import router from '@/router'
export const loadLoginUserInfo = () => {
  const token = localStorage.getItem('userToken')
  if (token) { // 登录-> 查询登录用户信息
    store.dispatch('setToken', token)
    instance.get('/back/userInfo').then((response) => {
      const res = response.data
      if (res.code === 0) {
        store.dispatch('setUserId', res.data.user_info.id)
        store.dispatch('setDeparts', res.data.depart_list)
        store.dispatch('setGroups', res.data.group_list)
      } else if (res.code === 2) {
        // 需要重新登录
        store.commit('setUserId', null)
        store.commit('userStatus', null)
        store.commit('setUserId', null)
        localStorage.setItem('userName', null)
        localStorage.setItem('userToken', null)
      }
    })
  }
}
export const exitLogin = (response) => {
  // 退出成功
  localStorage.setItem('userName', null)
  localStorage.setItem('userToken', null)
  store.commit('userStatus', null)
  store.commit('setToken', null)
  store.commit('setUserId', '')
  store.commit('setDeparts', [])
  store.commit('setGroups', [])
  store.commit('setPermissions', {})
  const url = window.location.pathname
  // if (url.indexOf('/backend') !== -1 && url !== '/schedule') { // 在退出前是后台管理页面
  //   alert('yo')
  //   router.push('/') // 返回首页
  // }
}

