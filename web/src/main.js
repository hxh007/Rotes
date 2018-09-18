// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import iView from 'iview'
import fullCalendar from 'vue-fullcalendar'
import 'iview/dist/styles/iview.css'
import '@/assets/common.css'
Vue.config.productionTip = false
Vue.use(iView)
Vue.component('full-calendar', fullCalendar)
Vue.prototype.bus = new Vue()

axios.defaults.timeout = 6000 // 6000的超时验证
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8'
const instance = axios.create()
instance.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8'
axios.interceptors.request.use = instance.interceptors.request.use

// request拦截器
instance.interceptors.request.use(
  config => {
    // 每次发送请求之前都检测vuex是否存有token,有的话都要放在请求头发送给服务器
    if (store.state.token) {
      config.headers.Authorization = `token ${store.state.token}`
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)
// response拦截器
instance.interceptors.response.use(
  response => { // 默认除了200以外的都是错误的，就会走这里
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          store.dispatch('userLogout') // 可能是token过期，清除它
          router.replace({ // 跳转到登录页面
            path: '/login',
            query: {
              redirect: router.currentRoute.fullPath
            }
          })
      }
    }
    return Promise.reject(error.response)
  }
)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  instance,
  components: {App},
  methods: {
    // 获取当前月的月份
    getCurrentMonth (string) {
      let date = new Date(string)
      return date.getMonth() + 1
    },
    // 格式化日期
    formatDate (fmt, date) {
      var o = {
        'M+': date.getMonth() + 1, // 月份
        'd+': date.getDate(), // 日
        'h+': date.getHours(), // 小时
        'm+': date.getMinutes(), // 分
        's+': date.getSeconds(), // 秒
        'q+': Math.floor((date.getMonth() + 3) / 3), // 季度
        'S': date.getMilliseconds() // 毫秒
      }
      if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
      }
      for (var k in o) {
        if (new RegExp('(' + k + ')').test(fmt)) {
          fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
        }
      }
      return fmt
    },
    getNowFormatDate () {
      var date = new Date()
      var seperator1 = '-'
      var year = date.getFullYear()
      var month = date.getMonth() + 1
      var strDate = date.getDate()
      if (month >= 1 && month <= 9) {
        month = '0' + month
      }
      if (strDate >= 0 && strDate <= 9) {
        strDate = '0' + strDate
      }
      var currentdate = year + seperator1 + month + seperator1 + strDate
      return currentdate
    }
  },
  template: '<App/>'
})
