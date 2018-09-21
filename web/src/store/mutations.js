export const userStatus = (state, user) => {
  if (user) {
    state.currentUser = user
    state.isLogin = true
  } else if (user === null) { // 登出
    // 登出的时候清空localStorage里的东西
    localStorage.setItem('userName', null)
    localStorage.setItem('userToken', null)
    state.currentUser = ''
    state.isLogin = false
    state.token = ''
  }
}
export const setToken = (state, token) => {
  state.token = token
}
export const setDeparts = (state, departs) => {
  state.myDepartments = departs
}
export const setGroups = (state, groups) => {
  state.myGroups = groups
}
