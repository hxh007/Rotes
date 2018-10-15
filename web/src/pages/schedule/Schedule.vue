<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">排班详情</h3>
      <Button v-bind:class="{'hidden-export': !showBackend}" type="primary" :style="{float: 'right', marginLeft: '20px'}" @click="exportScheduleList">
        导出排班表
      </Button>
      <div class="dateRange-box" :style="{float: 'right'}">
        <span>查询日期范围</span>
        <DatePicker type="daterange" v-model="dateRange" @on-change="changeDateRange" split-panels placeholder="Select date" style="width: 200px"></DatePicker>
      </div>
    </div>
    <Divider/>
    <div class="ivu-table-wrapper">
      <div class="ivu-table ivu-table-default ivu-table-border">
        <div class="ivu-table-overflowY ivu-table-overflowX">
          <div class="ivu-table-header" :style="{width: tableWidth}">
            <table cellspacing="0" cellpadding="0" border="0">
              <colgroup>
                <col :width="colWidth" v-for="(item, index) in tableHead" :key="index">
              </colgroup>
              <thead>
              <tr>
                <th v-for="(item, index) in tableHead" :key="index">
                  <div class="ivu-table-cell">
                    <span class="">{{item}}</span>
                  </div>
                </th>
              </tr>
              </thead>
            </table>
          </div>
          <div class="ivu-table-body" style="height: 100%">
            <table cellspacing="0" cellpadding="0" border="0" :style="{width: tableWidth}">
              <colgroup>
                <col :width="colWidth" v-for="(item, index) in tableHead" :key="index">
              </colgroup>
              <tbody class="ivu-table-tbody">
              <tr class="ivu-table-row"  v-for="(item, index) in tableList" :key="index">
                <td :width="colWidth" :rowspan="item.departNameRowspan" :colspan="item.departNameColspan" v-if="item.departNameShow">
                  <div class="ivu-table-cell" :class="{center: item.isCenter}">
                    <span>{{item.departName}}</span>
                  </div>
                </td>
                <td :width="colWidth" :rowspan="item.managersRowspan" :colspan="item.managersColspan" v-if="item.managersShow">
                  <div class="ivu-table-cell">
                    <span>{{item.managers}}</span>
                  </div>
                </td>
                <td :width="colWidth" :rowspan="item.roleNameRowspan" v-if="item.roleNameShow">
                  <div class="ivu-table-cell">
                    <span>{{item.roleName}}</span>
                  </div>
                </td>
                <td :width="colWidth" v-for="(innerItem, index) in item.dates" :key="index">
                  <div class="ivu-table-cell">
                    <span>{{innerItem}}</span>
                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
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
      dateRange: [],
      colWidth: '',
      tableWidth: '',
      tableHead: ['部门', '部门负责人', '角色']
    }
  },
  methods: {
    changeDateRange () {
      const startYear = this.dateRange[0].getFullYear()
      const startMonth = this.dateRange[0].getMonth()
      const startDay = this.dateRange[0].getDate()
      const endYear = this.dateRange[1].getFullYear()
      const endMonth = this.dateRange[1].getMonth()
      const endDay = this.dateRange[1].getDate()
      const startDate = this.$root.formatDate('yyyy-MM-dd', new Date(startYear, startMonth, startDay))
      const endDate = this.$root.formatDate('yyyy-MM-dd', new Date(endYear, endMonth, endDay))
      this.dateRange = [startDate, endDate]
      instance.get('/back/dutyinfo', {
        params: {
          dateStart: this.dateRange[0],
          dateEnd: this.dateRange[1]
        }
      }).then(this.loadDefaultDuties)
    },
    loadDefaultDuties (response) {
      let res = response.data
      this.tableHead = ['部门', '部门负责人', '角色']
      if (res.code === 0) {
        // 给表头赋值
        res.data.dateList.forEach((item, index) => {
          this.tableHead.push(item)
        })
        // 头部以及表格宽度的确定
        if (res.data.dateList.length > 5) {
          this.tableWidth = 100 * parseInt(res.data.dateList.length + 3) + 'px'
          this.colWidth = 100
        } else {
          let len = res.data.dateList.length + 3
          this.tableWidth = '100%'
          this.colWidth = (100 / len) + '%'
        }
        // 渲染表格体数据
        this.loadDefaultTbody(res.data.dateList, res.data.dutyInfo)
      } else {
        this.$Message.error(res.msg)
      }
    },
    loadDefaultTbody (dateList, dutyInfo) {
      this.tableList = []
      // 先渲染值班总监
      for (let departItem in dutyInfo) {
        if (departItem === '三、四线部门') {
          for (let dutyItem in dutyInfo[departItem]) {
            if (Object.keys(dutyInfo[departItem]).length > 2) {
              if (dutyItem === '四线值班') {
                let obj = {
                  departName: '值班总监',
                  departNameRowspan: 1,
                  departNameShow: true,
                  departNameColspan: 3,
                  managers: '',
                  managersRowspan: 1,
                  managersShow: false,
                  managersColspan: 3,
                  roleName: '',
                  roleNameRowspan: 1,
                  roleNameShow: false,
                  dates: {},
                  isCenter: true
                }
                dateList.forEach((date, index) => {
                  obj.dates[date] = dutyInfo[departItem][dutyItem][date] ? dutyInfo[departItem][dutyItem][date][0] : '--'
                })
                this.tableList.push(obj)
              }
            } else { // = 2 只有count和managerList
              let obj2 = {
                departName: '三、四线值班',
                departNameRowspan: 1,
                departNameShow: true,
                departNameColspan: 3,
                managers: '',
                managersRowspan: 1,
                managersShow: false,
                managersColspan: 3,
                roleName: '',
                roleNameRowspan: 1,
                roleNameShow: false,
                dates: {}
              }
              dateList.forEach((date, index) => {
                obj2.dates[date] = '--'
              })
              this.tableList.push(obj2)
            }
          }
        }
      }
      // 再排三线
      for (let departItem in dutyInfo) {
        if (departItem === '三、四线部门') {
          for (let dutyItem in dutyInfo[departItem]) {
            if (Object.keys(dutyInfo[departItem]).length > 2) {
              if (dutyItem === '三线值班') {
                let obj = {
                  departName: '三线值班',
                  departNameRowspan: 1,
                  departNameShow: true,
                  departNameColspan: 3,
                  managers: '',
                  managersRowspan: 1,
                  managersShow: false,
                  managersColspan: 3,
                  roleName: '',
                  roleNameRowspan: 1,
                  roleNameShow: false,
                  dates: {},
                  isCenter: true
                }
                dateList.forEach((date, index) => {
                  obj.dates[date] = dutyInfo[departItem][dutyItem][date] ? dutyInfo[departItem][dutyItem][date][0] : '--'
                })
                this.tableList.push(obj)
              }
            } else { // = 2 只有count和managerList
              let obj2 = {
                departName: '三、四线值班',
                departNameRowspan: 1,
                departNameShow: true,
                departNameColspan: 3,
                managers: '',
                managersRowspan: 1,
                managersShow: false,
                managersColspan: 3,
                roleName: '',
                roleNameRowspan: 1,
                roleNameShow: false,
                dates: {}
              }
              dateList.forEach((date, index) => {
                obj2.dates[date] = '--'
              })
              this.tableList.push(obj2)
            }
          }
        }
      }
      // 再排系统运维部
      for (let departItem in dutyInfo) {
        if (departItem === '系统运维部') {
          let departCount = dutyInfo[departItem].count
          if (Object.keys(dutyInfo[departItem]).length > 2) { // 当前部门已经安排有角色 ： 一线， 二线 ...
            for (let detailItem in dutyInfo[departItem]) {
              if (detailItem !== 'count' && detailItem !== 'managerList') {
                let dutyRoleCount = dutyInfo[departItem][detailItem]['count'] // 每个部门所对应角色应有的值班记录条数
                for (let i = 0; i <= dutyInfo[departItem][detailItem]['count'] - 1; i++) { // 遍历每个角色的值班人员
                  let dataObj = {
                    departName: departItem,
                    departNameRowspan: dutyInfo[departItem].count,
                    departNameShow: departCount === dutyInfo[departItem].count,
                    departNameColspan: 1,
                    managers: dutyInfo[departItem]['managerList'].length > 0 ? dutyInfo[departItem]['managerList'].join(' ') : '',
                    managersRowspan: dutyInfo[departItem].count,
                    managersShow: departCount === dutyInfo[departItem].count,
                    managersColspan: 1,
                    roleName: detailItem,
                    roleNameRowspan: dutyInfo[departItem][detailItem]['count'],
                    roleNameShow: dutyRoleCount === dutyInfo[departItem][detailItem]['count'],
                    isCenter: false,
                    dates: {}
                  }
                  dateList.forEach((date, index) => {
                    if (!dutyInfo[departItem][detailItem][date]) {
                      // 如果这一天该值班角色没有值班记录
                      dataObj.dates[date] = '--'
                    } else { // 有值班记录
                      dataObj.dates[date] = dutyInfo[departItem][detailItem][date][i] ? dutyInfo[departItem][detailItem][date][i] : '--'
                    }
                  })
                  this.tableList.push(dataObj)
                  dutyRoleCount--
                  departCount--
                }
              }
            }
          } else { // 当前部门并没有安排角色，只有count和managerList
            // 说明当前只有count与managerList这两个键，该部门还未安排任何角色
            let emptyRoleObj = {
              departName: departItem,
              departNameRowspan: 1,
              departNameShow: true,
              departNameColspan: 1,
              managers: dutyInfo[departItem]['managerList'].length > 0 ? dutyInfo[departItem]['managerList'].join(' ') : '',
              managersRowspan: 1,
              managersShow: true,
              managersColspan: 1,
              roleName: '',
              roleNameRowspan: 1,
              roleNameShow: true,
              isCenter: false,
              dates: {}
            }
            dateList.forEach((date, index) => {
              emptyRoleObj.dates[date] = '--'
            })
            this.tableList.push(emptyRoleObj)
          }
        }
      }
      // 再排网络安全部
      for (let departItem in dutyInfo) {
        if (departItem === '网络安全部') {
          let departCount = dutyInfo[departItem].count
          if (Object.keys(dutyInfo[departItem]).length > 2) { // 当前部门已经安排有角色 ： 一线， 二线 ...
            for (let detailItem in dutyInfo[departItem]) {
              if (detailItem !== 'count' && detailItem !== 'managerList') {
                let dutyRoleCount = dutyInfo[departItem][detailItem]['count'] // 每个部门所对应角色应有的值班记录条数
                for (let i = 0; i <= dutyInfo[departItem][detailItem]['count'] - 1; i++) { // 遍历每个角色的值班人员
                  let netDataObj = {
                    departName: departItem,
                    departNameRowspan: dutyInfo[departItem].count,
                    departNameShow: departCount === dutyInfo[departItem].count,
                    departNameColspan: 1,
                    managers: dutyInfo[departItem]['managerList'].length > 0 ? dutyInfo[departItem]['managerList'].join(' ') : '',
                    managersRowspan: dutyInfo[departItem].count,
                    managersShow: departCount === dutyInfo[departItem].count,
                    managersColspan: 1,
                    roleName: detailItem,
                    roleNameRowspan: dutyInfo[departItem][detailItem]['count'],
                    roleNameShow: dutyRoleCount === dutyInfo[departItem][detailItem]['count'],
                    isCenter: false,
                    dates: {}
                  }
                  dateList.forEach((date, index) => {
                    if (!dutyInfo[departItem][detailItem][date]) {
                      // 如果这一天该值班角色没有值班记录
                      netDataObj.dates[date] = '--'
                    } else { // 有值班记录
                      netDataObj.dates[date] = dutyInfo[departItem][detailItem][date][i] ? dutyInfo[departItem][detailItem][date][i] : '--'
                    }
                  })
                  this.tableList.push(netDataObj)
                  dutyRoleCount--
                  departCount--
                }
              }
            }
          } else { // 当前部门并没有安排角色，只有count和managerList
            // 说明当前只有count与managerList这两个键，该部门还未安排任何角色
            let netEmptyRoleObj = {
              departName: departItem,
              departNameRowspan: 1,
              departNameShow: true,
              departNameColspan: 1,
              managers: dutyInfo[departItem]['managerList'].length > 0 ? dutyInfo[departItem]['managerList'].join(' ') : '',
              managersRowspan: 1,
              managersShow: true,
              managersColspan: 1,
              roleName: '',
              roleNameRowspan: 1,
              roleNameShow: true,
              isCenter: false,
              dates: {}
            }
            dateList.forEach((date, index) => {
              netEmptyRoleObj.dates[date] = '--'
            })
            this.tableList.push(netEmptyRoleObj)
          }
        }
      }
      // 再排其他部门
      for (let departItem in dutyInfo) {
        if (departItem !== '三、四线部门' && departItem !== '系统运维部' && departItem !== '网络安全部') {
          let departCount = dutyInfo[departItem].count
          if (Object.keys(dutyInfo[departItem]).length > 2) { // 当前部门已经安排有角色 ： 一线， 二线 ...
            for (let detailItem in dutyInfo[departItem]) {
              if (detailItem !== 'count' && detailItem !== 'managerList') {
                let dutyRoleCount = dutyInfo[departItem][detailItem]['count'] // 每个部门所对应角色应有的值班记录条数
                for (let i = 0; i <= dutyInfo[departItem][detailItem]['count'] - 1; i++) { // 遍历每个角色的值班人员
                  let otherDataObj = {
                    departName: departItem,
                    departNameRowspan: dutyInfo[departItem].count,
                    departNameShow: departCount === dutyInfo[departItem].count,
                    departNameColspan: 1,
                    managers: dutyInfo[departItem].managerList.length > 0 ? dutyInfo[departItem].managerList.join(' ') : '',
                    managersRowspan: dutyInfo[departItem].count,
                    managersShow: departCount === dutyInfo[departItem].count,
                    managersColspan: 1,
                    roleName: detailItem,
                    roleNameRowspan: dutyInfo[departItem][detailItem]['count'],
                    roleNameShow: dutyRoleCount === dutyInfo[departItem][detailItem]['count'],
                    isCenter: false,
                    dates: {}
                  }
                  dateList.forEach((date, index) => {
                    if (!dutyInfo[departItem][detailItem][date]) {
                      // 如果这一天该值班角色没有值班记录
                      otherDataObj.dates[date] = '--'
                    } else { // 有值班记录
                      otherDataObj.dates[date] = dutyInfo[departItem][detailItem][date][i] ? dutyInfo[departItem][detailItem][date][i] : '--'
                    }
                  })
                  this.tableList.push(otherDataObj)
                  dutyRoleCount--
                  departCount--
                }
              }
            }
          } else { // 当前部门并没有安排角色，只有count和managerList
            // 说明当前只有count与managerList这两个键，该部门还未安排任何角色
            let otherEmptyRoleObj = {
              departName: departItem,
              departNameRowspan: 1,
              departNameShow: true,
              departNameColspan: 1,
              managers: dutyInfo[departItem]['managerList'].length > 0 ? dutyInfo[departItem]['managerList'].join(' ') : '',
              managersRowspan: 1,
              managersShow: true,
              managersColspan: 1,
              roleName: '',
              roleNameRowspan: 1,
              roleNameShow: true,
              isCenter: false,
              dates: {}
            }
            dateList.forEach((date, index) => {
              otherEmptyRoleObj.dates[date] = '--'
            })
            this.tableList.push(otherEmptyRoleObj)
          }
        }
      }
    },
    exportScheduleList () {
      const dateStart = this.$root.formatDate('yyyy-MM-dd', this.dateRange[0])
      const dateEnd = this.$root.formatDate('yyyy-MM-dd', this.dateRange[1])
      console.log(dateStart, dateEnd)
      instance.post('/back/datatoxlsx', {
        dateStart: dateStart,
        dateEnd: dateEnd
      }, {
        responseType: 'blob'
      }).then((response) => {
        let res = response.data
        this.downloadFile(res, 'Rotas_' + dateStart + '_' + dateEnd)
      })
    }
  },
  computed: {
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
    }
  },
  mounted () {
    // 给默认值
    const year = new Date().getFullYear()
    const month = new Date().getMonth() + 1
    const dateStart = this.$root.formatDate('yyyy-MM-dd', new Date([year, month, '01'].join('-')))
    const dateEnd = this.$root.formatDate('yyyy-MM-dd', new Date([year, month, new Date(year, month, 0).getDate()].join('-')))
    this.dateRange = [dateStart, dateEnd]
    console.log(this.dateRange[0], this.dateRange[1])
    instance.get('/back/dutyinfo', {
      params: {
        dateStart: this.dateRange[0],
        dateEnd: this.dateRange[1]
      }
    }).then(this.loadDefaultDuties)
  }
}
</script>

<style scoped lang="stylus">
.search-box
  margin-top 20px
.hidden-export
  display none
</style>
