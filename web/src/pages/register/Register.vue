<template>
  <div class="register-container">
    <div class="register-form">
      <div class="logo-title">
        <h1>Rotas</h1>
      </div>
      <div class="form-detail">
        <div class="form-register">
          <Form ref="formItem" :model="formItem" :rules="ruleFormItem">
            <FormItem prop="username">
              <Input type="text" v-model="formItem.username" placeholder="用户名">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
              </Input>
            </FormItem>
            <FormItem prop="fullname">
              <Input type="text" v-model="formItem.fullname" placeholder="姓名">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
              </Input>
            </FormItem>
            <FormItem prop="mobile">
              <Input type="text" v-model="formItem.mobile" placeholder="手机">
                <Icon type="ios-call-outline" slot="prepend"></Icon>
              </Input>
            </FormItem>
            <FormItem prop="passwd">
            <Input type="password" v-model="formItem.passwd" placeholder="6-20位以字母开头，只能包含字母和数字">
              <Icon type="ios-lock-outline" slot="prepend"></Icon>
            </Input>
          </FormItem>
            <FormItem prop="passwdCheck">
              <Input type="password" v-model="formItem.passwdCheck" placeholder="确认密码">
                <Icon type="ios-lock-outline" slot="prepend"></Icon>
              </Input>
            </FormItem>
            <FormItem>
              <Col span="12">
                <Button type="primary" @click="handleSubmit('formItem')" :class="[registerBtn]">注册</Button>
              </Col>
              <Col span="12" :style="{paddingLeft: '30px', paddingTop: '5px'}">
                <router-link to="/login" class="goToLogin">已有账号，前往登陆</router-link>
              </Col>
            </FormItem>
          </Form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'Register',
  data () {
    const validateTel = (rule, value, callback) => {
      if (rule.pattern.test(value)) { // 匹配正则验证
        callback()
      } else {
        callback(new Error('请输入正确格式的手机号码!'))
      }
    }
    const validatePass = (rule, value, callback) => {
      if (!rule.pattern.test(value)) {
        callback(new Error('6-20位以字母开头，只能包含字母和数字!'))
      } else {
        if (this.formItem.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.formItem.validateField('passwdCheck')
        }
        callback()
      }
    }
    const validatePassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码！'))
      } else if (value !== this.formItem.passwd) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      registerBtn: 'register-btn',
      formItem: {
        username: '',
        fullname: '',
        mobile: '',
        passwd: '',
        passwdCheck: ''
      },
      ruleFormItem: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        fullname: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        mobile: [
          { required: true, message: '请输入正确的手机号', trigger: 'blur' },
          { type: 'Number', pattern: /^1[34578]\d{9}$/, validator: validateTel }
        ],
        passwd: [
          { required: true, message: '请输入密码.', trigger: 'blur' },
          { type: 'string', pattern: /^[a-zA-Z]\w{6,22}$/, validator: validatePass }
        ],
        passwdCheck: [
          { required: true, message: '请输入密码.', trigger: 'blur' },
          { type: 'string', min: 6, validator: validatePassCheck, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.post('/back/register', {
            client_type: 100,
            fullname: this.formItem.fullname,
            username: this.formItem.username,
            mobile: this.formItem.mobile,
            password: this.formItem.passwd
          }).then(this.registerSuccessCallback)
        }
      })
    },
    registerSuccessCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('注册成功，快去登陆吧！')
        this.$router.push('/login')
      } else {
        this.$Message.error(res.msg)
      }
    }
  }
}
</script>

<style scoped lang="stylus">
  body,html
    font-size 14px
    font-family "Microsoft YaHei"
  .register-container
    width 100%
    background url(../../assets/bg.png) center no-repeat
    margin 0 auto
    background-size 100% 100%
    min-height 100vh
    .register-form
      width 400px
      min-height 400px
      border-radius 2px
      position absolute
      top 8%
      left 50%
      margin-left -200px
      z-index 100
      overflow hidden
      .form-detail
        position relative
        background #fff
        height 420px
        .form-register
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
      .register-btn
        height 37px
        line-height 27px
        width 138px
        border-radius 0
        background #313b4c
        color #ffffff
        border none
        font-size 20px
</style>
