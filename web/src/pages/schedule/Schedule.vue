<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">排班详情[整月]</h3>
    </div>
    <Divider/>
  </div>
</template>

<script>
// import instance from  '../../../libs/axios'
export default {
  name: 'Schedule',
  data () {
    return {

    }
  },
  mounted () {
    // console.log(this.$route.query.dateRange)
  }
}
</script>

<style scoped lang="stylus">
.search-box
  margin-top 20px
</style>
