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
    <Menu active-name="1-2" theme="dark" width="auto" :open-names="[]">
      <Submenu name="1">
        <template slot="title">
          <Icon type="ios-navigate"></Icon>
          Item 1
        </template>
        <MenuItem name="1-1">Option 1</MenuItem>
        <MenuItem name="1-2">Option 2</MenuItem>
        <MenuItem name="1-3">Option 3</MenuItem>
      </Submenu>
      <Submenu name="2">
        <template slot="title">
          <Icon type="ios-keypad"></Icon>
          Item 2
        </template>
        <MenuItem name="2-1">Option 1</MenuItem>
        <MenuItem name="2-2">Option 2</MenuItem>
      </Submenu>
      <Submenu name="3">
        <template slot="title">
          <Icon type="ios-analytics"></Icon>
          后台管理
        </template>
        <MenuItem name="3-1">
          <router-link tag="li" to="/backend/userManage">
            用户管理
          </router-link>
        </MenuItem>
        <MenuItem name="3-2">
          <router-link tag="li" to="/backend/permissionManage">
            权限管理
          </router-link>
        </MenuItem>
        <MenuItem name="3-3">
          <router-link tag="li" to="/backend/departManage">
            部门管理
          </router-link>
        </MenuItem>
        <MenuItem name="3-4">角色管理</MenuItem>
        <MenuItem name="3-5">分组管理</MenuItem>
        <MenuItem name="3-6">
          <router-link tag="li" to="/backend/operationManage">
            操作管理
          </router-link>
        </MenuItem>
      </Submenu>
    </Menu>
  </div>
</template>

<script>
export default {
  name: 'AppMenu',
  props: {
    isCollapse: Boolean
  },
  computed: {
    menuitemClasses () {
      return [
        'menu-item',
        this.isCollapse ? 'collapsed-menu' : ''
      ]
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
</style>
