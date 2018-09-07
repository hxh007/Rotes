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
    <home-modal :show="departOneModal" :currentDay="currentDay"></home-modal>
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
      toggleShow: true,
      flag: 1// 1--所有部门，0--当前用户所属部门
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
      this.bus.$emit('dayClickWatch', this.departOneModal)// 往子组件传递控制模态框显示与否的开关切换
      this.searchDetail()
    },
    getDutySucc (data) {
      let res = data.data
      if (res.code === 0 && res.data) {
        console.log(res.data)
        this.fcEvents = res.data
      }
    },
    getDuties () {
      let departId = this.flag === 1 ? undefined : this.$store.state.departId
      console.log(this.monthviewFisrt, this.monthviewLast, departId)
      axios.get('/api/arrangeDuty.json', {
        params: {
          departId: departId,
          dateRange: [this.monthviewFisrt, this.monthviewLast]
        }
      }).then(this.getDutySucc)
    },
    changeToggleFunc () {
      this.flag = this.toggleShow === true ? 1 : 0
    },
    searchDetail () {
      // 先判断当前是显示所有部门的还是本部门的 1---所有部门 0---当前部门
      let departId = this.flag === 1 ? undefined : this.$store.state.departId
      let dateRange = [this.currentDay, this.currentDay]
      console.log(departId, dateRange)
      // axios.get('/api/search', {
      //   params: {
      //     departId: this.$store.state.departId || undefined,
      //     dateRange: [monthviewFisrt, monthviewLast]
      //   }
      // }).then()
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
</style>
