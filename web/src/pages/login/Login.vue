<template>
  <div class="login-container">
    <div class="login-form" id="login-form">
      <div class="logo-title">
        <h1>Rotas</h1>
      </div>
      <div class="form-detail">
        <div class="form-login">
          <Form ref="formItem" :model="formItem" :rules="ruleFormItem">
            <FormItem prop="user">
              <Input type="text" v-model="formItem.user" placeholder="用户名">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
              </Input>
            </FormItem>
            <FormItem prop="password">
              <Input type="password" v-model="formItem.password" placeholder="密码">
                <Icon type="ios-lock-outline" slot="prepend"></Icon>
              </Input>
            </FormItem>
            <FormItem>
              <Col span="12">
                <Button type="primary" @click="handleSubmit('formItem')" :class="[loginBtn]">登录</Button>
              </Col>
              <Col span="12">
                <a class="scanLogin" @click="ddLogin">钉钉扫码登录</a>
              </Col>
            </FormItem>
            <FormItem>
              <router-link to="/register" class="goToRegister">没有账号？前往注册</router-link>
            </FormItem>
          </Form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
import { mapMutations } from 'vuex'
import { DDLogin } from '../../../libs/util'
// import store from '@/store'
export default {
  name: 'Login',
  data () {
    return {
      loginBtn: 'login-btn',
      formItem: {
        user: '',
        password: ''
      },
      ruleFormItem: {
        user: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码.', trigger: 'blur' },
          { type: 'string', min: 6, message: '密码长度不得低于6位', trigger: 'blur' }
        ]
      },
      urlCommon: ''
    }
  },
  methods: {
    ...mapMutations([
      'setToken'
    ]),
    handleSubmit (name) { // 登录
      this.$refs[name].validate((valid) => {
        if (valid) { // 表单验证通过
          instance.post('/back/login', {
            username: this.formItem.user,
            password: this.formItem.password,
            client_type: 100
          }).then(response => {
            const res = response.data
            const data = res.data
            if (res.code === 0) {
              // 改变vuex 中的状态
              localStorage.setItem('userName', data.user.username)
              localStorage.setItem('userToken', data.jwt_token)
              this.$store.dispatch('setUser', data.user.username)
              this.$store.dispatch('setUserId', data.user.id)
              this.$store.dispatch('setToken', 'JWT ' + data.jwt_token)
              this.$store.dispatch('setPermissions', data.permission_list)
              this.$store.dispatch('setDeparts', data.depart_list)
              this.$store.dispatch('setGroups', data.group_list)
              this.$router.push('/')
            } else {
              this.$Message.error(res.msg)
            }
          })
        }
      })
    },
    ddLogin () {
      // 初始化钉钉登录
      if (typeof window.addEventListener !== 'undefined') {
        window.addEventListener('message', this.handleMessage, false)
      } else if (typeof window.attachEvent !== 'undefined') {
        window.attachEvent('onmessage', this.handleMessage)
      }
      this.$Spin.show()
      let host = document.domain
      let port = window.location.port
      let urlHead = port ? host + ':' + port : host
      instance.get('/back/dd_login_params').then((response) => {
        let res = response.data
        let url = 'https://oapi.dingtalk.com/connect/oauth2/sns_authorize?appid=' + res.appid +
          '&response_type=' + res.response_type + '&scope=' + res.scope + '&state=http://' + urlHead + '&redirect_uri=http://' + urlHead + res.redirect_uri
        this.urlCommon = url
        this.$Spin.hide()
        DDLogin({
          id: 'login-form', // 这里需要你在自己的页面定义一个HTML标签并设置id，例如<div id="login_container"></div>或<span id="login_container"></span>
          goto: encodeURIComponent(url),
          width: '400',
          height: '400'
        })
      })
    },
    handleMessage () {
      let origin = event.origin
      console.log('origin', event.origin)
      if (origin === 'https://login.dingtalk.com') { // 判断是否来自ddLogin扫码事件。
        let loginTmpCode = event.data // 拿到loginTmpCode后就可以在这里构造跳转链接进行跳转了
        if (loginTmpCode) {
          console.log('loginTmpCode', loginTmpCode)
          window.location.href = this.urlCommon + '&loginTmpCode=' + loginTmpCode
        }
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    next()
  },
  mounted () {
    document.onkeydown = (ev) => {
      let key = ev.key
      if (key === 'Enter') {
        this.handleSubmit('formItem')
      }
    }
  }
}
</script>

<style scoped lang="stylus">
body,html
  font-size 14px
  font-family "Microsoft YaHei"
.login-container
  width 100%
  background url(../../assets/bg.png) center no-repeat
  margin 0 auto
  background-size 100% 100%
  min-height 100vh
  .login-form
    width 400px
    min-height 400px
    border-radius 2px
    position absolute
    top 17%
    left 50%
    margin-left -200px
    z-index 100
    overflow hidden
    .form-detail
      position relative
      background #fff
      height 279px
      .form-login
        width 100%
        padding 58px 55px 0 56px
    .logo-title
      width 100%
      height 121px
      line-height 121px
      border-radius 2px 2px 0 0
      background #313b4c
      text-align center
      line-height 121px
      color #ffffff
      font-size 30px
  .ivu-form-item-content
    height 37px
    line-height 37px
    .login-btn
      height 37px
      line-height 27px
      width 138px
      border-radius 0
      background #313b4c
      color #ffffff
      border none
      font-size 20px
    .scanLogin
      margin-left 40px
      height 30px
      line-height 40px
      font-size 16px
    .goToRegister
      color #313b4c
</style>
