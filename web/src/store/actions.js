export const setUser = ({commit}, user) => {
  commit('userStatus', user)
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
