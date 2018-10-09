<template>
  <Row>
    <Col class="demo-spin-col" span="24">
      <Spin fix>
        <Icon type="ios-loading" size=50 class="demo-spin-icon-load"></Icon>
        <div class="tip">扫码成功，正在跳转...</div>
      </Spin>
    </Col>
  </Row>
</template>

<script>
import { GetQueryString } from '../../../libs/util'
import instance from '../../../libs/axios'
export default {
  name: 'oauth_callback',
  mounted () {
    let code = GetQueryString('code')
    instance.post('/back/login', {
      client_type: 200,
      code: code
    }).then((response) => {
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
}
</script>

<style scoped lang="stylus">
  .demo-spin-icon-load{
    animation: ani-demo-spin 1s linear infinite;
  }
  @keyframes ani-demo-spin {
    from { transform: rotate(0deg);}
    50%  { transform: rotate(180deg);}
    to   { transform: rotate(360deg);}
  }
  .demo-spin-col{
    height: 100vh;
    position: relative;
  }
  .tip
    font-size 24px
</style>
