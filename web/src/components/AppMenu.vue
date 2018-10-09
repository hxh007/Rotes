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
    <Menu :active-name="activeName" theme="dark" width="auto" :open-names="openNames">
      <MenuItem name="/schedule" tag="li">
        <router-link tag="li" to="/schedule">
          <Icon type="ios-navigate"></Icon>
          <span>排班记录</span>
        </router-link>
      </MenuItem>
      <Submenu name="/backend" v-if="showBackend">
        <template slot="title">
          <Icon type="ios-analytics"></Icon>
          后台管理
        </template>
        <MenuItem name="/backend/adminManage" v-if="this.$root.whetherAdmin() || this.$root.whetherAdmin() && showMessManage">
          <router-link tag="li" to="/adminManage">
            管理组
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/userManage" v-if="showBackend">
          <router-link tag="li" to="/userManage">
            用户管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/permissionManage" v-if="this.$root.whetherAdmin() || this.$root.whetherAdmin() && showMessManage">
          <router-link tag="li" to="/permissionManage">
            权限管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/departManage" v-if="showBackend">
          <router-link tag="li" to="/departManage">
            部门管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/roleManage" v-if="this.$root.whetherAdmin() || this.$root.whetherAdmin() && showMessManage">
          <router-link tag="li" to="/roleManage">
            角色管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/operationManage" v-if="this.$root.whetherAdmin() || this.$root.whetherAdmin() && showMessManage">
          <router-link tag="li" to="/operationManage">
            操作管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/planTaskManage" v-if="this.$root.whetherAdmin() || this.$root.whetherAdmin() && showMessManage">
          <router-link tag="li" to="/planTaskManage">
            计划任务管理
          </router-link>
        </MenuItem>
        <MenuItem name="/backend/messageManage" v-if="showBackend">
          <router-link tag="li" to="/messageManage">
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
      subMenus: [],
      openNames: [],
      activeName: ''
    }
  },
  methods: {
    openFlagArray () {
      this.openNames = []
      if (this.$route.path.indexOf('Manage') !== -1) {
        this.openNames.push('/backend')
        this.activeName = '/backend' + this.$route.path
      } else {
        this.activeName = this.$route.path
      }
    }
  },
  props: {
    isCollapse: Boolean
  },
  computed: {
    menuitemClasses () {
      return [
        'menu-item',
        this.isCollapse ? 'collapsed-menu' : ''
      ]
    },
    showBackend () {
      if (this.$store.state.isLogin) { // 已登录
        // 然后再根据角色进行划分
        if (this.$store.state.myGroups.length > 0) {
          const admin = this.$root.whetherAdmin()
          const businessManager = this.$root.whetherBusiManager()
          if (admin || businessManager) {
            return true
          } else {
            return false
          }
        }
      } else { // 未登录
        return false
      }
    },
    showMessManage () {
      const busiManger = this.$root.whetherBusiManager()
      if (busiManger) {
        return true
      }
      return false
    }
  },
  watch: {
    $route () {
      this.openFlagArray()
    }
  },
  mounted () {
    this.openFlagArray()
    console.log(this.activeName, this.openNames)
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
