// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import iView from 'iview'
import fullCalendar from 'vue-fullcalendar'
import 'iview/dist/styles/iview.css'
import '@/assets/common.css'

Vue.config.productionTip = false
Vue.use(iView)
Vue.component('full-calendar', fullCalendar)
Vue.prototype.bus = new Vue()
Vue.prototype.downloadFile = function (data, name) {
  if (!data) {
    return
  }
  let url = window.URL.createObjectURL(new Blob([data]))
  let link = document.createElement('a')
  link.style.display = 'none'
  link.href = url
  link.setAttribute('download', name + '.xlsx')
  document.body.appendChild(link)
  link.click()
}
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
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
    },
    whetherAdmin () {
      const myGroups = store.state.myGroups
      let flag = 0
      if (myGroups.length > 0) { // 当前用户拥有最少一个所属部门
        for (let i = 0; i < myGroups.length; i++) {
          if (myGroups[i].name === 'S_MANAGEMENT') {
            flag += 1
          }
        }
      }
      if (flag > 0) { // 为超级管理员
        return true
      } else {
        return false
      }
    },
    whetherBusiManager () {
      const myGroups = store.state.myGroups
      let flag = 0
      if (myGroups.length > 0) { // 当前用户拥有最少一个所属部门
        for (let i = 0; i < myGroups.length; i++) {
          if (myGroups[i].name === 'BU_MANAGEMENT') {
            flag += 1
          }
        }
      }
      if (flag > 0) { // 为业务管理员
        return true
      } else {
        return false
      }
    }
  },
  template: '<App/>'
})
