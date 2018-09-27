import axios from 'axios'
let instance = axios.create()
const token  = localStorage.getItem('userToken')
instance.defaults.headers = {
  'X-Requested-With': 'XMLHttpRequest',
  'Authorization': 'JWT ' + token
}
export default instance
