<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden', verticalAlign: 'bottom', float: 'left', marginBottom: '10px'}">
      <router-link to="/backend/planTaskManage" :style="{float: 'left', fontSize: '18px', marginRight: '10px'}">
        <Icon type="md-arrow-back" :style="{color: '#5cadff'}" />
        <a>定时任务</a>
      </router-link>
      <h3 :style="{fontSize: '16px', 'float': 'left', borderLeft: '1px solid #666', paddingTop: '1px', paddingLeft: '10px'}">创建定时任务</h3>
    </div>
    <Divider/>
    <div class="timing-task">
      <h3>基本信息</h3>
      <Row :style="{marginTop: '20px', marginLeft: '10px', marginBottom: '10px'}">
        <Col span="12" offset="1">
          <Form ref="formItem" :rules="ruleValidate" :model="formItem" :label-width="80">
            <FormItem label="任务名称" prop="name">
              <Input v-model="formItem.name" placeholder="任务名称"></Input>
            </FormItem>
            <FormItem label="工具" prop="selectedFunc">
              <Select v-model="formItem.selectedFunc">
                <Option v-for="(item, key) in formItem.funcs" :value="item.func" :key="key">{{item.info}}</Option>
              </Select>
            </FormItem>
            <FormItem label="执行时间" prop="task">
              <Input v-model="formItem.time" disabled>
                <span slot="append" :style="{cursor: 'pointer'}" @click="selectTimeRule">选择时间规则</span>
              </Input>
            </FormItem>
          </Form>
        </Col>
      </Row>
      <h3>参数</h3>
      <Row>
        <Col offset="2">
          该工具无参数，请直接执行
        </Col>
      </Row>
      <Divider/>
      <Button type="primary" @click="createTimeTask('formItem')">提交</Button>
    </div>
    <Modal
      v-model="timeFlag"
      title="选择时间规则"
      @on-ok="confirmTimeRule"
      @on-cancel="cancelTimeRule">
      <Tabs :style="{marginBottom: '20px'}">
        <TabPane label="秒">
          <RadioGroup vertical v-model="secondMode" @on-change="changeSecondsMode">
            <Radio label="wildcard">
              <span>分钟，允许的通配符【,-*/】</span>
            </Radio>
            <Radio label="assign">
              <span>指定</span>
            </Radio>
          </RadioGroup>
          <CheckboxGroup :style="{padding: '0 20px'}" v-model="selectedSeconds" @on-change="changeSecondsChoice">
            <Checkbox v-for="(item, index) in assignSeconds" :label="item" :key="index"></Checkbox>
          </CheckboxGroup>
        </TabPane>
        <TabPane label="分钟">
          <RadioGroup vertical v-model="minuteMode" @on-change="changeMinuteMode">
            <Radio label="wildcard">
              <span>分钟，允许的通配符【,-*/】</span>
            </Radio>
            <Radio label="assign">
              <span>指定</span>
            </Radio>
          </RadioGroup>
          <CheckboxGroup :style="{padding: '0 20px'}" v-model="selectedMinutes" @on-change="changeMinutesChoice">
            <Checkbox v-for="(item, index) in assignMinutes" :label="item" :key="index"></Checkbox>
          </CheckboxGroup>
        </TabPane>
        <TabPane label="小时">
          <RadioGroup vertical v-model="hourMode" @on-change="changeHourMode">
            <Radio label="wildcard">
              <span>分钟，允许的通配符【,-*/】</span>
            </Radio>
            <Radio label="assign">
              <span>指定</span>
            </Radio>
          </RadioGroup>
          <CheckboxGroup :style="{padding: '0 20px'}" v-model="selectedHours" @on-change="changeHoursChoice">
            <Checkbox v-for="(item, index) in assignHours" :label="item" :key="index"></Checkbox>
          </CheckboxGroup>
        </TabPane>
        <TabPane label="日">
          <RadioGroup vertical v-model="dayMode" @on-change="changeDayMode">
            <Radio label="wildcard">
              <span>分钟，允许的通配符【,-*/】</span>
            </Radio>
            <Radio label="assign">
              <span>指定</span>
            </Radio>
          </RadioGroup>
          <CheckboxGroup :style="{padding: '0 20px'}" v-model="selectedDays" @on-change="changeDaysChoice">
            <Checkbox v-for="(item, index) in assignDays" :label="item" :key="index"></Checkbox>
          </CheckboxGroup>
        </TabPane>
        <TabPane label="月">
          <RadioGroup vertical v-model="monthMode" @on-change="changeMonthMode">
            <Radio label="wildcard">
              <span>分钟，允许的通配符【,-*/】</span>
            </Radio>
            <Radio label="assign">
              <span>指定</span>
            </Radio>
          </RadioGroup>
          <CheckboxGroup :style="{padding: '0 20px'}" v-model="selectedMonths" @on-change="changeMonthChoice">
            <Checkbox v-for="(item, index) in assignMonths" :label="item" :key="index"></Checkbox>
          </CheckboxGroup>
        </TabPane>
        <TabPane label="周">
          <RadioGroup vertical v-model="weekMode" @on-change="changeWeekMode">
            <Radio label="wildcard">
              <span>分钟，允许的通配符【,-*/】</span>
            </Radio>
            <Radio label="assign">
              <span>指定</span>
            </Radio>
          </RadioGroup>
          <CheckboxGroup :style="{padding: '0 20px'}" v-model="selectedWeeks" @on-change="changeWeeksChoice">
            <Checkbox v-for="(item, index) in assignWeeks" :label="item" :key="index"></Checkbox>
          </CheckboxGroup>
        </TabPane>
      </Tabs>
      <div class="timerule-box" :style="{border: '1px solid #ccc', height: '50px'}">
        <div class="tip-text">时间表达式</div>
        <div class="time-formula">
          <span>{{second}}</span>&nbsp;
          <span>{{minute}}</span>&nbsp;
          <span>{{hour}}</span>&nbsp;
          <span>{{day}}</span>&nbsp;
          <span>{{month}}</span>&nbsp;
          <span>{{week}}</span>&nbsp;
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'CreateTimingTask',
  data () {
    return {
      timeFlag: false,
      secondMode: 'wildcard',
      minuteMode: 'wildcard',
      hourMode: 'wildcard',
      dayMode: 'wildcard',
      monthMode: 'wildcard',
      weekMode: 'wildcard',
      formItem: {
        name: '',
        funcs: [],
        time: '* * * * * *',
        selectedFunc: '',
        assignMinutes: []
      },
      assignSeconds: [],
      assignMinutes: [],
      assignHours: [],
      assignDays: [],
      assignMonths: [],
      assignWeeks: ['星期一', ' 星期二', '星期三', '星期四', '星期五', '星期六', '星期日'],
      selectedSeconds: [],
      selectedMinutes: [],
      selectedHours: [],
      selectedDays: [],
      selectedMonths: [],
      selectedWeeks: [],
      ruleValidate: {
        name: [
          { required: true, message: '任务名称！', trigger: 'blur' }
        ],
        selectedFunc: [
          { required: true, message: '请选择! ', trigger: 'change' }
        ]
      },
      second: '*',
      minute: '*',
      hour: '*',
      day: '*',
      month: '*',
      week: '*'
    }
  },
  computed: {
    selectedSecondsFunc () {
      return this.selectedSeconds.length
    },
    selectedMinutesFunc () {
      return this.selectedMinutes.length
    },
    selectedHoursFunc () {
      return this.selectedHours.length
    },
    selectedDaysFunc () {
      return this.selectedDays.length
    },
    selectedMonthsFunc () {
      return this.selectedMonths.length
    },
    selectedWeeksFunc () {
      return this.selectedWeeks.length
    }
  },
  watch: {
    selectedSecondsFunc (new_) {
      if (new_ > 0) {
        this.secondMode = 'assign'
        this.second = this.selectedSeconds.join(',')
      }
      if (new_ === 0) {
        this.second = '*'
      }
    },
    selectedMinutesFunc (new_) {
      if (new_ > 0) {
        this.minuteMode = 'assign'
        this.minute = this.selectedMinutes.join(',')
      }
      if (new_ === 0) {
        this.minute = '*'
      }
    },
    selectedHoursFunc (new_) {
      if (new_ > 0) {
        this.hourMode = 'assign'
        this.hour = this.selectedHours.join(',')
      }
      if (new_ === 0) {
        this.hour = '*'
      }
    },
    selectedDaysFunc (new_) {
      if (new_ > 0) {
        this.dayMode = 'assign'
        this.day = this.selectedDays.join(',')
      }
      if (new_ === 0) {
        this.day = '*'
      }
    },
    selectedMonthsFunc (new_) {
      if (new_ > 0) {
        this.monthMode = 'assign'
        this.month = this.selectedMonths.join(',')
      }
      if (new_ === 0) {
        this.month = '*'
      }
    },
    selectedWeeksFunc (new_) {
      if (new_ > 0) {
        this.weekMode = 'assign'
        this.week = this.selectedWeeks.join(',')
      }
      if (new_ === 0) {
        this.week = '*'
      }
    }
  },
  methods: {
    loadFuncsCallback (response) {
      let res = response.data
      if (res.ret === 0) { // 获取数据成功
        this.formItem.funcs = res.detail
      } else { //  报错
        this.$Message.error('请求出错!')
      }
    },
    confirmTimeRule () {
      this.formItem.time = this.minute + ' ' + this.hour + ' ' + this.day + ' ' + this.month + ' ' + this.week
      this.timeFlag = false
    },
    cancelTimeRule () {
      this.timeFlag = false
    },
    selectTimeRule () {
      this.timeFlag = true
    },
    changeSecondsMode () {
      if (this.secondMode === 'wildcard') {
        this.selectedSeconds = []
      }
    },
    changeMinuteMode () {
      if (this.minuteMode === 'wildcard') {
        this.selectedMinutes = []
      }
    },
    changeHourMode () {
      if (this.hourMode === 'wildcard') {
        this.selectedHours = []
      }
    },
    changeDayMode () {
      if (this.hourMode === 'wildcard') {
        this.selectedDays = []
      }
    },
    changeMonthMode () {
      if (this.hourMode === 'wildcard') {
        this.selectedMonths = []
      }
    },
    changeWeekMode () {
      if (this.weekMode === 'wildcard') {
        this.selectedWeeks = []
      }
    },
    generateSeconds () {
      for (let i = 0; i < 60; i++) {
        this.assignSeconds.push(i)
      }
    },
    generateMinutes () {
      for (let i = 0; i < 60; i++) {
        this.assignMinutes.push(i)
      }
    },
    generateHours () {
      for (let i = 0; i < 24; i++) {
        this.assignHours.push(i)
      }
    },
    generateDays () {
      for (let i = 1; i <= 31; i++) {
        this.assignDays.push(i)
      }
    },
    generateMonths () {
      for (let i = 1; i <= 12; i++) {
        this.assignMonths.push(i)
      }
    },
    createSucccessCallback (response) {
      let res = response.data
      if (res.ret === 0) {
        this.$Message.success('定时任务创建成功！')
        // this.$refs['formItem'].resetFields()
      } else {
        this.$Message.error(res.msg)
      }
    },
    changeSecondsChoice (name) {
      this.selectedSeconds = []
      this.selectedSeconds.push(name[name.length - 1])
      this.second = name[name.length - 1]
    },
    changeMinutesChoice (name) {
      this.selectedMinutes = []
      this.selectedMinutes.push(name[name.length - 1])
      this.minute = name[name.length - 1]
    },
    changeHoursChoice (name) {
      this.selectedHours = []
      this.selectedHours.push(name[name.length - 1])
      this.hour = name[name.length - 1]
    },
    changeDaysChoice (name) {
      this.selectedDays = []
      this.selectedDays.push(name[name.length - 1])
      this.day = name[name.length - 1]
    },
    changeMonthChoice (name) {
      this.selectedMonths = []
      this.selectedMonths.push(name[name.length - 1])
      this.month = name[name.length - 1]
    },
    changeWeeksChoice (name) {
      this.selectedWeeks = []
      this.selectedWeeks.push(name[name.length - 1])
      this.week = name[name.length - 1]
    },
    createTimeTask (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          // 判断当前的周-》要传给后端的参数格式
          let week = this.week === '*' ? '*' : this.assignWeeks.indexOf(this.week)
          let paramObj = {
            trigger: 'cron',
            name: this.formItem.name,
            func: this.formItem.selectedFunc,
            second: this.second === '*' ? '*' : this.selectedSeconds.join(','),
            minute: this.minute === '*' ? '*' : this.selectedMinutes.join(','),
            hour: this.hour === '*' ? '*' : this.selectedHours.join(','),
            day: this.day === '*' ? '*' : this.selectedDays.join(','),
            month: this.month === '*' ? '*' : this.selectedMonths.join(','),
            day_of_week: week
          }
          instance.post('/back/cron/jobs', paramObj).then(this.createSucccessCallback)
        }
      })
    }
  },
  mounted () {
    // 渲染工具参数
    instance.get('/back/cron/funcs').then(this.loadFuncsCallback)
    // 生成秒数
    this.generateSeconds()
    // 生成分钟数【指定】
    this.generateMinutes()
    // 生成小时数【指定】
    this.generateHours()
    // 生成天数 【指定】
    this.generateDays()
    // 生成月份 【指定】
    this.generateMonths()
  }
}
</script>

<style scoped lang="stylus">
.timing-task
  margin-top 50px
.timerule-box
  position relative
.tip-text
  position absolute
  left 43%
  top -20%
  display inline-block
  background #ffffff
  padding 0 10px
.time-formula
  text-align center
  margin-top 16px
</style>
