import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userId: 0,
    username: '',
    roleId: 0,
    roleName: '',
    departId: 2,
    departName: '网络安全部'
  },
  mutations: {
    changeUserInfo (state, userInfo) {
      // 登录或者登出改变用户信息
    },
    changeDepartInfo (state, departInfo) {
      // 登录或者登出改变部门信息
    }
  }
})
