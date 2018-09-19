import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userId: localStorage.rotasUser ? JSON.parse(localStorage.getItem('rotasUser')).id : 0,
    username: localStorage.rotasUser ? JSON.parse(localStorage.getItem('rotasUser')).username : '',
    fullname: localStorage.rotasUser ? JSON.parse(localStorage.getItem('rotasUser')).fullname : '',
    token: localStorage.token ? localStorage.token : '',
    myDepartments: localStorage.myDepartments ? localStorage.myDepartments : [],
    myGroups: localStorage.myGroups ? localStorage.myGroups : []
  },
  mutations: {
    userLogin (state, payload) {
      // 用户登录
      localStorage.setItem('rotasUser', JSON.stringify(payload.user))
      localStorage.token = payload.jwt_token
      localStorage.myDepartments = payload.depart_list
      localStorage.myGroups = payload.group_list
    },
    userLogout (state, payload) {
      // 用户登出
    }
  }
})
