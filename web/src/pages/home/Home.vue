<template>
  <div>
    <full-calendar :events="fcEvents" locale="en" @changeMonth="changeMonthFunc"
                   @dayClick="dayClickFunc">
      <div slot="fc-header-right">
        <Row>
          <Col>
            <Select v-model="departSearch" style="width:200px" @on-change="changeOnSelect">
              <Option v-for="item in myDeparts" :value="item.id" :key="item.id">{{ item.label }}</Option>
            </Select>
          </Col>
        </Row>
      </div>
    </full-calendar>
    <home-modal :show="departOneModal" :currentDay="currentDay" :departSearch="departSearch"></home-modal>
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
      today: '', // 获取今日时间
      curMonthview: new Date().getMonth() + 1, // 获得点击的当月月份，8月,9月...,
      monthviewFisrt: this.$root.formatDate('yyyy-MM-dd', new Date([new Date().getFullYear(), new Date().getMonth() + 1, '01'].join('-'))),
      monthviewLast: this.$root.formatDate('yyyy-MM-dd', new Date([new Date().getFullYear(),
        new Date().getMonth() + 1,
        new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate()].join('-'))),
      tableList: [], // 用于渲染modal中的表格数据
      departsAllShowDetail: false, // 判断是否显示的是所有部门的某一天排班信息
      pNum: 0,
      departSearch: '--',
      myDeparts: []
    }
  },
  methods: {
    changeMonthFunc () {
      if (this.curMonthview !== this.$root.getCurrentMonth(arguments[2])) {
        this.curMonthview = this.$root.getCurrentMonth(arguments[2])
        this.monthviewFisrt = arguments[2]
        let year = new Date(arguments[2]).getFullYear()
        let month = new Date(arguments[2]).getMonth() + 1
        let days = new Date(year, month, 0).getDate()
        this.monthviewLast = this.$root.formatDate('yyyy-MM-dd', new Date([year, month, days].join('-')))
        this.getDuties()
      }
    },
    dayClickFunc () {
      this.currentDay = this.$root.formatDate('yyyy-MM-dd', arguments[0]) // 点击的具体某个日期
      let year = arguments[0].getFullYear() // 当前年
      let month = String(arguments[0].getMonth() + 1).length === 1 ? '0' + (arguments[0].getMonth() + 1) : (arguments[0].getMonth() + 1) // 当前月
      let days = arguments[0].getDate(year, month, 0) // 当前月的天数
      let start = [year, month, '01'].join('-')
      let end = [year, month, days].join('-')
      this.monthviewFisrt = start
      this.monthviewLast = end
      this.departOneModal = true
      if (this.departSearch === '--') { // 所有部门
        this.departsAllShowDetail = true // 显示出所有部门的值班记录
      } else if (this.departSearch !== '--' && this.departOneModal) { // 本部门
        this.bus.$emit('dayClickWatch', this.departOneModal)// 往子组件传递控制模态框显示与否的开关切换
      }
      this.searchDetail()
    },
    getDutySucc (data) {
      this.fcEvents = []
      let res = data.data
      if (res.code === 0 && res.data) {
        // this.fcEvents = res.data
        let departId = this.departSearch === '--' ? undefined : this.departSearch
        if (departId) { // 某个部门
          res.data.dateList.forEach((item, index) => { // 遍历排班的所有日期
            let dutyListData = res.data.dutyList
            if (dutyListData[item]) { // 该日有值班记录
              for (let dutyName in dutyListData[item]) {
                this.fcEvents.push({
                  'title': dutyName + '——' + dutyListData[item][dutyName] + '条记录',
                  'start': item,
                  'end': item
                })
              }
            } else { // 该日没有值班记录
              this.fcEvents.push({
                'title': '无值班记录',
                'start': item,
                'end': item,
                'cssClass': ['noRecord']
              })
            }
          })
        } else { // 所有部门
          // 先将departId,departName与本来应有的角色对应起来
          let perfectDepartInfo = []
          for (let dId in res.data.departInfo) {
            let myObj = {}
            myObj = {
              departId: dId,
              departName: res.data.departInfo[dId],
              roleLists: [] // 放应该有的roleId作对照用
            }
            for (let ddid in res.data.departRoles) {
              myObj.roleLists.push(res.data.departRoles[ddid])
            }
            perfectDepartInfo.push(myObj)
          }
          res.data.dateList.forEach((item, index) => { // 遍历排班的所有日期
            let dutyListData = res.data.dutyList
            if (dutyListData[item]) { // dutyListData[item] --- 系统运维部:{一线: 1}
              for (let i = 0; i < perfectDepartInfo.length; i++) {
                let roles = perfectDepartInfo[i].roleLists
                for (let dName in dutyListData[item]) {
                  if (dName === perfectDepartInfo[i].departName) { // 当前日期中有该部门的值班记录
                    roles.splice(roles.indexOf(dName), 1)
                  }
                }
                if (roles.length > 0) { // 说明当前部门有些排班角色还未提交完全
                  this.fcEvents.push({
                    title: perfectDepartInfo[i].departName,
                    start: item,
                    end: item,
                    cssClass: ['warnRecord']
                  })
                }
              }
            } else {
              this.fcEvents.push({
                'title': '无值班记录',
                'start': item,
                'end': item,
                'cssClass': ['noRecord']
              })
            }
          })
        }
      }
    },
    getDuties () { // 获取当前月份视图的所有未排班信息
      let departId = this.departSearch === '--' ? undefined : this.departSearch
      axios.get('/back/dutysCount', {
        params: {
          departId: departId,
          dateStart: this.monthviewFisrt,
          dateEnd: this.monthviewLast
        }
      }).then(this.getDutySucc)
    },
    changeOnSelect () {
      this.getDuties()
    },
    searchDetail () {
      // 先判断当前是显示所有部门的还是本部门的 1---所有部门 0---当前部门
      let departId = this.departSearch
      let dateStart = departId === 0 ? this.monthviewFisrt : this.currentDay
      let dateEnd = departId === 0 ? this.monthviewLast : this.currentDay
      axios.get('/back/dutyLists', {
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
        if (this.departSearch !== '--') { // 本部门之一
          let data = res.data[0]
          let count = 0
          let num
          data.roleList.forEach((item, index) => {
            for (let i in item) {
              if (i === 'dutyList') {
                num = 0
                item[i].forEach((ite, ind) => { // 排班角色
                  this.tableList.push({
                    'departId': data.departId,
                    'roleId': data.roleId,
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
                  count++
                })
              }
            }
          })
          this.bus.$emit('sendDepartData', this.tableList)
        } else { // 所有部门
          let num
          res.data.forEach((pData, pindex) => { // 遍历每个部门的值班信息
            this.pNum = 0
            pData.roleList.forEach((item, index) => { // 遍历每个部门下的每个角色，无论是否有值班记录
              for (let i in item) {
                if (i === 'dutyList') {
                  if (item.dutyList.length === 0) { // 某个角色下没有任何值班记录
                    this.tableList.push({
                      'departName': pData.departName,
                      'col1Rospan': pData.total,
                      'col1RospanShow': Boolean(this.pNum === 0),
                      'roleName': item.roleName,
                      'col2Rospan': 1,
                      'col2RospanShow': true,
                      'dutyName': '--'
                    })
                    ++this.pNum
                  } else {
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
                      ++this.pNum
                    })
                  }
                }
              }
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
    // 先根据是否登陆的vuex state信息，动态渲染右上角的查询条件
    // 为空的话则证明该用户没有登录 | 当前用户不属于任何一个部门 > 权限：只能浏览全部部门的值班信息
    // ---- 初始化操作
    this.myDeparts = [{
      id: '--',
      label: '所有部门'
    }]
    if (this.$store.state.myDepartments.length > 0) { // 说明当前登录用户属于多个部门
      this.$store.state.myDepartments.forEach((item, index) => {
        this.myDeparts.push({
          id: item.id,
          label: item.name
        })
      })
    }
    this.getDuties()
    this.bus.$on('refreshCalendar', () => {
      this.$router.go(0)
    })
    this.today = this.$root.getNowFormatDate()
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
