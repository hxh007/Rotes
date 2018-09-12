<template>
  <div>
    <full-calendar :events="fcEvents" locale="en" @changeMonth="changeMonthFunc"
                   @dayClick="dayClickFunc">
      <div slot="fc-header-right">
        <i-switch size="large" :style="{float: 'right'}" v-model="toggleShow"
                  @on-change="changeToggleFunc">
          <span slot="open">所有</span>
          <span slot="close">本部</span>
        </i-switch>
      </div>
    </full-calendar>
    <home-modal :show="departOneModal" :currentDay="currentDay" :tableList="tableList"></home-modal>
    <Modal width="60%"
      v-model="departsAllShowDetail"
      title="Common Modal dialog box title"
      @on-ok="ok"
      @on-cancel="cancel">
      <div slot="header">
        <h3>
          <Icon type="md-briefcase" />
          所有部门排班详情（{{currentDay}}）
        </h3>
      </div>
      <div class="ivu-table-wrapper">
        <div class="ivu-table ivu-table-default ivu-table-border">
          <div class="ivu-table-header">
            <table cellspacing="0" cellpadding="0" border="0" style="width: 100%">
              <colgroup>
                <col width="35%">
                <col width="30%">
                <col width="35%">
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
            <table cellspacing="0" cellpadding="0" border="0" style="width: 100%">
              <colgroup>
                <col width="35%">
                <col width="30%">
                <col width="35%">
              </colgroup>
              <tbody class="ivu-table-tbody">
              <tr class="ivu-table-row"  v-for="(item, index) in tableList" :key="index">
                <td :rowspan="item.col1Rospan" v-if="item.col1RospanShow">
                  <div class="ivu-table-cell">
                    <span>{{item.departName}}</span>
                  </div>
                </td>
                <td :rowspan="item.col2Rospan" v-if="item.col2RospanShow">
                  <div class="ivu-table-cell">
                    <span>{{item.roleName}}</span>
                  </div>
                </td>
                <td>
                  <div class="ivu-table-cell">
                    <span>{{item.dutyName}}</span>
                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>
<script>
import FullCalendar from 'vue-fullcalendar'
import axios from 'axios'
import HomeModal from './components/HomeModal'
export default {
  name: 'home',
  data () {
    return {
      departOneModal: false,
      fcEvents: [],
      currentDay: '', // 点击的具体某个日期
      curMonthview: new Date().getMonth() + 1, // 获得点击的当月月份，8月,9月...,
      monthviewFisrt: [new Date().getFullYear(), new Date().getMonth() + 1, '01'].join('-'),
      monthviewLast: [new Date().getFullYear(), new Date().getMonth() + 1,
        new Date().getDate(new Date().getFullYear(), new Date().getMonth() + 1, 0)].join('-'),
      toggleShow: Boolean(this.$store.state.userId),
      flag: 0, // 1--所有部门，0--当前用户所属部门
      tableList: [], // 用于渲染modal中的表格数据
      departsAllShowDetail: false, // 判断是否显示的是所有部门的某一天排班信息
      pNum: 0
    }
  },
  methods: {
    changeMonthFunc () {
      if (this.curMonthview !== this.$root.getCurrentMonth(arguments[2])) {
        this.curMonthview = this.$root.getCurrentMonth(arguments[2])
        this.getDuties()
      }
    },
    dayClickFunc () {
      this.currentDay = this.$root.formatDate('yyyy-MM-dd', arguments[0]) // 点击的具体某个日期
      let year = arguments[0].getFullYear() // 当前年
      let month = arguments[0].getMonth() + 1 // 当前月
      let days = arguments[0].getDate(year, month, 0) // 当前月的天数
      let start = [year, month, '01'].join('-')
      let end = [year, month, days].join('-')
      this.monthviewFisrt = start
      this.monthviewLast = end
      this.departOneModal = true
      if (this.flag === 1) { // 所有部门
        this.departsAllShowDetail = true
      } else if (this.flag === 0 && this.departOneModal) { // 本部门
        this.bus.$emit('dayClickWatch', this.departOneModal)// 往子组件传递控制模态框显示与否的开关切换
      }
      this.searchDetail()
    },
    getDutySucc (data) {
      let res = data.data
      if (res.code === 0 && res.data) {
        // this.fcEvents = res.data
        console.log(res)
        let departId = this.flag === 1 ? undefined : this.$store.state.departId
        res.data.dateList.forEach((item, index) => { // 遍历排班的所有日期
          let dutyListData = res.data.dutyList
          if (departId) { // 某个部门
            // let departRoles = res.data.departRoles // 某个部门才需要显示具体的角色
            for (let i in dutyListData) {
              console.log(i)
              if (i === item) { // 找到相同的日期
              }
            }
          } else {
          }
        })
      }
    },
    getDuties () { // 获取当前月份视图的所有未排班信息
      let departId = this.flag === 1 ? undefined : this.$store.state.departId
      axios.get('/back/duties', {
        params: {
          departId: departId,
          dateStart: this.monthviewFisrt,
          dateEnd: this.monthviewLast
        }
      }).then(this.getDutySucc)
    },
    changeToggleFunc () {
      this.flag = this.toggleShow === true ? 1 : 0
    },
    searchDetail () {
      // 先判断当前是显示所有部门的还是本部门的 1---所有部门 0---当前部门
      let departId = this.flag === 1 ? undefined : this.$store.state.departId
      let dateStart = departId === 0 ? this.monthviewFisrt : this.currentDay
      let dateEnd = departId === 0 ? this.monthviewLast : this.currentDay
      axios.get('/api/search.json', {
        params: {
          departId: departId,
          dateStart: dateStart,
          dateEnd: dateEnd
        }
      }).then(this.searchDetailCallback)
    },
    searchDetailCallback (response) {
      this.tableList = []
      let res = response.data
      if (res.code === 0) { // 返回正常
        if (this.flag === 0) { // 本部门
          let data = res.data[0]
          let count = 0
          let num
          data.roleList.forEach((item, index) => {
            for (let i in item) {
              if (i === 'dutyList') {
                num = 0
                item[i].forEach((ite, ind) => { // 排班角色
                  this.tableList.push({
                    'departName': data.departName,
                    'col1Rospan': data.total,
                    'col1RospanShow': Boolean(count === 0),
                    'roleName': item.roleName,
                    'col2Rospan': item.total,
                    'col2RospanShow': Boolean(num === 0),
                    'dutyName': ite.dutyName,
                    'dutyId': ite.dutyId
                  })
                  num++
                })
              }
            }
            count++
          })
        } else { // 所有部门
          let num
          res.data.forEach((pData, pindex) => { // 遍历每个部门的值班信息
            this.pNum = 0
            pData.roleList.forEach((item, index) => {
              for (let i in item) {
                if (i === 'dutyList') {
                  num = 0
                  item[i].forEach((ite, ind) => { // 排班角色
                    this.tableList.push({
                      'departName': pData.departName,
                      'col1Rospan': pData.total,
                      'col1RospanShow': Boolean(this.pNum === 0),
                      'roleName': item.roleName,
                      'col2Rospan': item.total,
                      'col2RospanShow': Boolean(num === 0),
                      'dutyName': ite.dutyName,
                      'dutyId': ite.dutyId
                    })
                    num++
                  })
                }
              }
              ++this.pNum
            })
          })
        }
      }
    },
    ok () {
      // this.$Message.info('Clicked ok')
    },
    cancel () {
      // this.$Message.info('Clicked cancel')
    }
  },
  components: {
    FullCalendar,
    HomeModal
  },
  mounted () {
    this.getDuties()
  }
}
</script>

<style lang="stylus">
  .events-week
    height 100px
    .event-box
      margin-top -8px
  .create-box
    padding 20px 50px
    overflow hidden
  .demo-drawer-profile{
    font-size: 14px;
  }
  .demo-drawer-profile .ivu-col{
    margin-bottom: 12px;
  }
</style>
