import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userId: 0,
    username: '',
    departId: 2,
    departName: '网络安全部',
    token: ''
  },
  mutations: {
    userLogout (state, payload) {
      // 用户登录
    },
    userLogin (state, payload) {
      // 用户登出
    }
  }
  //   changeUserInfo (state, userInfo) {
  //     // 登录或者登出改变用户信息
  //   },
  //   changeDepartInfo (state, departInfo) {
  //     // 登录或者登出改变部门信息
  //   }
  // }
})
