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
import instance from '../../../libs/axios'
export default {
  name: 'oauth_callback',
  mounted () {
    instance.post('/back/login', {
      client_type: 200
    }).then((response) => {
      console.log(response)
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
