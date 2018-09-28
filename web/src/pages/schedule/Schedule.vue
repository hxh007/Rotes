<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">排班详情</h3>
      <div class="dateRange-box" :style="{float: 'right'}">
        <span>查询日期范围</span>
        <DatePicker type="daterange" v-model="dateRange" @on-change="changeDateRange" split-panels placeholder="Select date" style="width: 200px"></DatePicker>
      </div>
    </div>
    <Divider/>
    <div class="ivu-table-wrapper">
      <div class="ivu-table ivu-table-default ivu-table-border">
        <div class="ivu-table-header" style="overflow-x: scroll">
          <table cellspacing="0" cellpadding="0" border="0">
            <colgroup>
              <col>
              <col>
              <col>
            </colgroup>
            <thead>
            <tr>
              <th>
                <div class="ivu-table-cell">
                  <span class="">部门名</span>
                </div>
              </th>
              <th>
                <div class="ivu-table-cell">
                  <span class="">排班角色</span>
                </div>
              </th>
              <th>
                <div class="ivu-table-cell">
                  <span class="">值班人员</span>
                </div>
              </th>
            </tr>
            </thead>
          </table>
        </div>
        <div class="ivu-table-body ivu-table-overflowY" style="height: 100%">
          <table cellspacing="0" cellpadding="0" border="0">
            <colgroup>
              <col>
              <col>
              <col>
            </colgroup>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'Schedule',
  data () {
    return {
      tableList: [],
      dateRange: []
    }
  },
  methods: {
    changeDateRange () {
      console.log(arguments)
    }
  },
  mounted () {
    // 给默认值
    const year = new Date().getFullYear()
    const month = new Date().getMonth() + 1
    const dateStart = this.$root.formatDate('yyyy-MM-dd', new Date([year, month, '01'].join('-')))
    const dateEnd = this.$root.formatDate('yyyy-MM-dd', new Date([year, month, new Date(year, month, 0).getDate()].join('-')))
    this.dateRange = [dateStart, dateEnd]
    instance.get('')
  }
}
</script>

<style scoped lang="stylus">
.search-box
  margin-top 20px
</style>
