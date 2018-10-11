export const setUser = ({commit}, user) => {
  commit('userStatus', user)
}
export const setNickName = ({commit}, nick) => {
  commit('setNickName', nick)
}
export const setUserId = ({commit}, userId) => {
  commit('setUserId', userId)
}
export const setToken = ({commit}, token) => {
  commit('setToken', token)
}
export const setDeparts = ({commit}, departs) => {
  commit('setDeparts', departs)
}
export const setGroups = ({commit}, groups) => {
  commit('setGroups', groups)
}
export const setPermissions = ({commit}, permissions) => {
  commit('setPermissions', permissions)
}
