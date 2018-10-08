import instance from 'axios'
import store from '@/store'
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
export const exitLogin = ( params ) => {
  // 退出成功
  localStorage.setItem('userName', null)
  localStorage.setItem('userToken', null)
  store.commit('userStatus', null)
  store.commit('setToken', null)
  store.commit('setUserId', '')
  store.commit('setDeparts', [])
  store.commit('setGroups', [])
  store.commit('setPermissions', {})
}
export const DDLogin = (a) => {
  var e, c = document.createElement("iframe"),
  d = "https://login.dingtalk.com/login/qrcode.htm?goto=" + a.goto ;
  d += a.style ? "&style=" + encodeURIComponent(a.style) : "",
  d += a.href ? "&href=" + a.href : "",
  c.src = d,
  c.frameBorder = "0",
  c.allowTransparency = "true",
  c.scrolling = "no",
  c.width =  a.width ? a.width + 'px' : "365px",
  c.height = a.height ? a.height + 'px' : "400px",
  e = document.getElementById(a.id),
  e.innerHTML = "",
  e.appendChild(c)
}
export const GetQueryString = (name) => {
  let reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)")
  let r = window.location.search.substr(1).match(reg)
  if(r!=null) {
    return  unescape(r[2])
  }
  return null
}

