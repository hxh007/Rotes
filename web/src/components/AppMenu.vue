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
  <Menu active-name="1-2" theme="dark" width="auto" :class="menuitemClasses">
      <MenuItem name="1-1">
        <Icon type="ios-navigate"></Icon>
        <span>Option 1</span>
      </MenuItem>
      <MenuItem name="1-2">
        <Icon type="ios-search"></Icon>
        <span>Option 2</span>
      </MenuItem>
      <MenuItem name="1-3">
        <Icon type="ios-settings"></Icon>
        <span>Option 3</span>
      </MenuItem>
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
