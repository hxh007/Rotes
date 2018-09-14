<template>
  <div class="">
    <div class="layout-logo-left">
      <router-link to="/">
        <span v-if="!isCollapse === true">
          Rotas
        </span>
        <span v-if="isCollapse === true">R</span>
      </router-link>
    </div>
    <Menu :active-name="activeMenu" theme="dark" width="auto" :open-names="openFlagArray">
      <MenuItem name="/schedule" tag="li">
        <router-link tag="li" to="/schedule">
          <Icon type="ios-navigate"></Icon>
          <span>排班记录</span>
        </router-link>
      </MenuItem>
      <Submenu name="backend">
        <template slot="title">
          <Icon type="ios-analytics"></Icon>
          后台管理
        </template>
        <MenuItem name="/backend/adminManage">
          <router-link tag="li" to="/backend/adminManage">
            管理员
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/userManage">
          <router-link tag="li" to="/backend/userManage">
            用户管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/permissionManage">
          <router-link tag="li" to="/backend/permissionManage">
            权限管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/departManage">
          <router-link tag="li" to="/backend/departManage">
            部门管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/roleManage">
          <router-link tag="li" to="/backend/roleManage">
            角色管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/operationManage">
          <router-link tag="li" to="/backend/operationManage">
            操作管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/messageManage">
          <router-link tag="li" to="/backend/messageManage">
            短信模板
          </router-link>
        </MenuItem>
      </Submenu>
    </Menu>
  </div>
</template>

<script>
export default {
  name: 'AppMenu',
  data () {
    return {
      subMenus: ['backend']
    }
  },
  props: {
    isCollapse: Boolean
  },
  watch: {
    $route (to, from) {
      console.log(to.path)
    }
  },
  computed: {
    menuitemClasses () {
      return [
        'menu-item',
        this.isCollapse ? 'collapsed-menu' : ''
      ]
    },
    activeMenu () {
      return this.$route.path
    },
    openFlagArray () {
      let arr = []
      this.subMenus.forEach((item, index) => {
        if (this.$route.path.indexOf(item) !== -1) {
          arr.push(item)
        }
      })
      return arr
    }
  }
}
</script>

<style scoped lang="stylus">
  .layout-logo-left
    width: 90%;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    margin: 15px auto;
    text-align: center;
    line-height: 30px;
    font-size: 20px;
    font-weight: 900;
  .menu-icon
    transition: all .3s
  .menu-item span
    display: inline-block
    overflow: hidden
    width: 69px
    text-overflow: ellipsis
    white-space: nowrap
    vertical-align: bottom
    transition: width .2s ease .2s
  .menu-item i
    transform: translateX(0px)
    transition: font-size .2s ease, transform .2s ease
    vertical-align: middle
    font-size: 16px
  .collapsed-menu span
    width: 0px
    transition: width .2s ease
  .collapsed-menu i
    transform: translateX(5px)
    transition: font-size .2s ease .2s, transform .2s ease .2s
    vertical-align: middle
    font-size: 22px
  .show
    color #000
  .ivu-menu-item
    padding 0!important
    li
      padding 14px 24px 14px 24px
      .ivu-icon
        margin-right 8px!important
  .ivu-menu-submenu
    font-size normal
    .ivu-menu-item
      padding 0
      padding-left 0!important
      li
        padding 14px 24px 14px 43px
</style>
