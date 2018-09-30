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
                <td :rowspan="item.departNameRowspan" :colspan="item.departNameColspan" v-if="item.departNameShow">
                  <div class="ivu-table-cell" :class="{center: item.isCenter}">
                    <span>{{item.departName}}</span>
                  </div>
                </td>
                <td :rowspan="item.managersRowspan" :colspan="item.managersColspan" v-if="item.managersShow">
                  <div class="ivu-table-cell">
                    <span>{{item.managers}}</span>
                  </div>
                </td>
                <td :rowspan="item.roleNameRowspan" v-if="item.roleNameShow">
                  <div class="ivu-table-cell">
                    <span>{{item.roleName}}</span>
                  </div>
                </td>
                <td v-for="(innerItem, key, index) in item.dates" :key="index">
                  <div class="ivu-table-cell" v-for="(ite,ind) in innerItem" :key="ind">
                    <span>{{ite}}</span>
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
          this.colWidth = parseInt(100 / len) + '%'
        }
        // 渲染表格体数据
        this.loadDefaultTbody(res.data.dateList, res.data.dutyInfo)
      } else {
        this.$Message.error(res.msg)
      }
    },
    loadDefaultTbody (dateList, dutyInfo) {
      this.tableList = []
      // 先渲染值班总监与三线
      for (let departItem in dutyInfo) {
        if (departItem === '三、四线部门') {
          for (let dutyItem in dutyInfo[departItem]) {
            if (Object.keys(dutyInfo[departItem]).length > 2) {
              if (dutyItem === '四线值班' || dutyItem === '三线值班') {
                let obj = {
                  departName: dutyItem === '四线值班' ? '值班总监' : '三线值班',
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
                  dates: [],
                  isCenter: true
                }
                dateList.forEach((date, index) => {
                  if (dutyInfo[departItem][dutyItem][date]) {
                    let piece = {}
                    piece[date] = dutyInfo[departItem][dutyItem][date][0]
                    obj.dates.push(piece)
                  } else {
                    let piece2 = {}
                    piece2[date] = '--'
                    obj.dates.push(piece2)
                  }
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
                dates: []
              }
              dateList.forEach((date, index) => {
                let emptyPiece = {}
                emptyPiece[date] = '--'
                obj2.dates.push(emptyPiece)
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
          let countFlag = 0
          for (let detailItem in dutyInfo[departItem]) {
            if (Object.keys(dutyInfo[departItem]).length > 2) {
              // 当前部门有相应的角色
              if (detailItem !== 'count' && detailItem !== 'managerList') { // 筛选出部门下面的排班角色
                let dutyRoleCount = dutyInfo[departItem][detailItem]['count'] // 1
                for (let i = 0; i <= dutyInfo[departItem][detailItem]['count'] - 1; i++) { // 遍历每一条值班记录
                  let dataObj = {
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
                    dates: []
                  }
                  dateList.forEach((date, index) => {
                    if (!dutyInfo[departItem][detailItem][date]) {
                      // 如果这一天该值班角色没有值班记录
                      let piece = {}
                      piece[date] = '--'
                      dataObj.dates.push(piece)
                    } else { // 有值班记录
                      let piece2 = {}
                      piece2[date] = dutyInfo[departItem][detailItem][date][i] ? dutyInfo[departItem][detailItem][date][i] : '--'
                      dataObj.dates.push(piece2)
                    }
                  })
                  this.tableList.push(dataObj)
                  dutyRoleCount -= 1
                }
              }
            } else { // 当前部门没有相应的角色
              if ((detailItem === 'count' || detailItem === 'managerList') && countFlag === 0) {
                // 说明当前只有count与managerList这两个键，该部门还未安排任何角色
                let emptyRoleObj = {
                  departName: departItem,
                  departNameRowspan: 1,
                  departNameShow: true,
                  departNameColspan: 1,
                  managers: dutyInfo[departItem].managerList.length > 0 ? dutyInfo[departItem].managerList.join(' ') : '',
                  managersRowspan: 1,
                  managersShow: true,
                  managersColspan: 1,
                  roleName: '',
                  roleNameRowspan: 1,
                  roleNameShow: true,
                  isCenter: false,
                  dates: []
                }
                dateList.forEach((date, index) => {
                  let piece = {}
                  piece[date] = dutyInfo[departItem][detailItem][date] ? dutyInfo[departItem][detailItem][date] : ''
                  emptyRoleObj.dates.push(piece)
                })
                this.tableList.push(emptyRoleObj)
                countFlag++
              }
            }
            departCount -= 1
          }
        }
      }
      // 再排网络安全部
      for (let departItem in dutyInfo) {
        if (departItem === '网络安全部') {
          let departCount = dutyInfo[departItem].count
          let countFlag = 0
          for (let detailItem in dutyInfo[departItem]) {
            if (Object.keys(dutyInfo[departItem]).length > 2) {
              // 当前部门有相应的角色
              if (detailItem !== 'count' && detailItem !== 'managerList') { // 筛选出部门下面的排班角色
                let dutyRoleCount = dutyInfo[departItem][detailItem]['count'] // 1
                for (let i = 0; i <= dutyInfo[departItem][detailItem]['count'] - 1; i++) { // 遍历每一条值班记录
                  let dataObj = {
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
                    dates: []
                  }
                  dateList.forEach((date, index) => {
                    if (!dutyInfo[departItem][detailItem][date]) {
                      // 如果这一天该值班角色没有值班记录
                      let piece = {}
                      piece[date] = '--'
                      dataObj.dates.push(piece)
                    } else { // 有值班记录
                      let piece2 = {}
                      piece2[date] = dutyInfo[departItem][detailItem][date][i] ? dutyInfo[departItem][detailItem][date][i] : '--'
                      dataObj.dates.push(piece2)
                    }
                  })
                  this.tableList.push(dataObj)
                  dutyRoleCount -= 1
                }
              }
            } else { // 当前部门没有相应的角色
              if ((detailItem === 'count' || detailItem === 'managerList') && countFlag === 0) {
                // 说明当前只有count与managerList这两个键，该部门还未安排任何角色
                let emptyRoleObj = {
                  departName: departItem,
                  departNameRowspan: 1,
                  departNameShow: true,
                  departNameColspan: 1,
                  managers: dutyInfo[departItem].managerList.length > 0 ? dutyInfo[departItem].managerList.join(' ') : '',
                  managersRowspan: 1,
                  managersShow: true,
                  managersColspan: 1,
                  roleName: '',
                  roleNameRowspan: 1,
                  roleNameShow: true,
                  isCenter: false,
                  dates: []
                }
                dateList.forEach((date, index) => {
                  let piece = {}
                  piece[date] = dutyInfo[departItem][detailItem][date] ? dutyInfo[departItem][detailItem][date] : '--'
                  emptyRoleObj.dates.push(piece)
                })
                this.tableList.push(emptyRoleObj)
                countFlag++
              }
            }
            departCount -= 1
          }
        }
      }
      // 再排其他部门的
      for (let departItem in dutyInfo) {
        if (departItem !== '三、四线部门' && departItem !== '系统运维部' && departItem !== '网络安全部') {
          let departCount = dutyInfo[departItem].count
          let countFlag = 0
          for (let detailItem in dutyInfo[departItem]) {
            if (Object.keys(dutyInfo[departItem]).length > 2) {
              // 当前部门有相应的角色
              if (detailItem !== 'count' && detailItem !== 'managerList') { // 筛选出部门下面的排班角色
                let dutyRoleCount = dutyInfo[departItem][detailItem]['count'] // 1
                for (let i = 0; i <= dutyInfo[departItem][detailItem]['count'] - 1; i++) { // 遍历每一条值班记录
                  let dataObj = {
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
                    dates: []
                  }
                  dateList.forEach((date, index) => {
                    if (!dutyInfo[departItem][detailItem][date]) {
                      // 如果这一天该值班角色没有值班记录
                      let piece = {}
                      piece[date] = '--'
                      dataObj.dates.push(piece)
                    } else { // 有值班记录
                      let piece2 = {}
                      piece2[date] = dutyInfo[departItem][detailItem][date][i] ? dutyInfo[departItem][detailItem][date][i] : '--'
                      dataObj.dates.push(piece2)
                    }
                  })
                  this.tableList.push(dataObj)
                  dutyRoleCount -= 1
                }
              }
            } else { // 当前部门没有相应的角色
              if ((detailItem === 'count' || detailItem === 'managerList') && countFlag === 0) {
                // 说明当前只有count与managerList这两个键，该部门还未安排任何角色
                let emptyRoleObj = {
                  departName: departItem,
                  departNameRowspan: 1,
                  departNameShow: true,
                  departNameColspan: 1,
                  managers: dutyInfo[departItem].managerList.length > 0 ? dutyInfo[departItem].managerList.join(' ') : '',
                  managersRowspan: 1,
                  managersShow: true,
                  managersColspan: 1,
                  roleName: '',
                  roleNameRowspan: 1,
                  roleNameShow: true,
                  isCenter: false,
                  dates: []
                }
                dateList.forEach((date, index) => {
                  let piece = {}
                  piece[date] = dutyInfo[departItem][detailItem][date] ? dutyInfo[departItem][detailItem][date] : '--'
                  emptyRoleObj.dates.push(piece)
                })
                this.tableList.push(emptyRoleObj)
                countFlag++
              }
            }
            departCount -= 1
          }
        }
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
</style>
