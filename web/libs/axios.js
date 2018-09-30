import axios from 'axios'
import store from '@/store'
let instance = axios.create()
let token = ''
const testLogin = () => {
  if (store.state.isLogin === true && store.state.token) {
    token  = localStorage.getItem('userToken')
  }
}

instance.interceptors.request.use(config => {
  testLogin()
  if (token) {
    config.headers.Authorization = 'JWT ' + token
  } else {
    config.headers.Authorization = ''
  }
  return config
}, error => {
  Promise.reject(error)
})
export default instance
