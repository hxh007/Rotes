import Vue from 'vue'
import Vuex from 'vuex'
import * as mutations from './mutations'
import * as actions from './actions'
import * as getters from './getters'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUserId: '',
    currentUser: '',
    nickName: '',
    isLogin: false,
    token: '',
    myDepartments: [],
    myGroups: [],
    myPermissions: {}
  },
  mutations,
  actions,
  getters
})
