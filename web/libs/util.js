import axios from 'axios'
import store from '@/store'
export const loadLoginUserInfo = () => {
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
        console.log(res.data)
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
// export const axiosRequest = (url, method, paramObj, success, error) => { // 添加公共头部
//   const token = localStorage.getItem('userToken')
//   if (method === 'GET' || method === 'get') {
//     axios.get(url, {
//       headers: {
//         Authorization: 'JWT ' + token
//       },
//       params: paramObj
//     }).then(success)
//   } else {
//     axios.method
//   }
// }

