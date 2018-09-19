<template>
  <Modal v-model="departOneModalCopy" fullscreen>
    <div slot="header">
      <h3>
        <Icon type="md-briefcase" />
        排班详情（{{currentDay}}）
      </h3>
    </div>
    <Row style="background:#eee;padding:20px;height: 100%">
      <Col span="12" :style="{'height': '100%'}">
        <Card shadow :style="{'height': '100%'}">
          <p slot="title">排班详情</p>
          <div class="ivu-table-wrapper">
            <div class="ivu-table ivu-table-default ivu-table-with-fixed-top">
              <div class="ivu-table-header">
                <table cellspacing="0" cellpadding="0" border="0" style="width: 680px">
                  <colgroup>
                    <col width="200">
                    <col width="200">
                    <col width="200">
                    <col width="74">
                    <col width="17">
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
                    <th>
                      <div class="ivu-table-cell">
                        <span class="">操作</span>
                      </div>
                    </th>
                    <th rowspan="1"></th>
                  </tr>
                  </thead>
                </table>
              </div>
              <div class="ivu-table-body ivu-table-overflowY" style="height: 100%" v-if="dutyLists.length !== 0">
                <table cellspacing="0" cellpadding="0" border="0" style="width: 663px">
                  <colgroup>
                    <col width="200">
                    <col width="200">
                    <col width="200">
                    <col width="72">
                  </colgroup>
                  <tbody class="ivu-table-tbody">
                  <tr class="ivu-table-row"  v-for="(item, index) in dutyLists" :key="index">
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
                    <td>
                      <div class="ivu-table-cell">
                      <span>
                        <Button type="error" size="small" @click="deleteDutyRecord(item.dutyId)">删除</Button>
                      </span>
                      </div>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
              <div class="ivu-table-tip" style="" v-else>
                <table cellspacing="0" cellpadding="0" border="0">
                  <tbody>
                  <tr>
                    <td style="width: 591px">
                      <span>暂无数据</span>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </Card>
      </Col>
      <Col span="11" offset="1"  :style="{'height': '100%'}">
        <Card :bordered="false" :style="{'height': '100%'}">
          <p slot="title">新建排班</p>
          <div class="create-box" ref="createBox">
            <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
              <FormItem label="所属部门">
                <h3>{{this.$store.state.departName}}</h3>
              </FormItem>
              <FormItem label="排班角色">
                <Select v-model="selectRole">
                  <Option v-for="item in roleLists" :value="item.id" :key="item.id">{{ item.label }}</Option>
                </Select>
              </FormItem>
              <FormItem label="选择人员" prop="staff">
                <Select v-model="selectStaff">
                  <Option v-for="item in staffLists" :value="item.staffId" :key="item.staffId">{{ item.label }}</Option>
                </Select>
              </FormItem>
              <FormItem>
                <Button type="primary" @click="handleSubmit('formValidate')">提交</Button>
                <Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button>
              </FormItem>
            </Form>
          </div>
        </Card>
      </Col>
    </Row>
    <div slot="footer">
      <Button type="primary" size="large" @click="cancelModal">确定</Button>
    </div>
  </Modal>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HomeModal',
  data () {
    return {
      childTableList: [],
      formValidate: {
        role: '',
        staff: ''
      },
      ruleValidate: {
      },
      departOneModalCopy: false,
      staffLists: [],
      roleLists: [],
      selectStaff: '',
      selectRole: '',
      dutyLists: []
    }
  },
  props: {
    departOneModal: Boolean,
    currentDay: String,
    tableList: Array,
    departSearch: String
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          axios.post('/back/duty', {
            departId: this.departSearch, // 能进来的一定是有部门的
            dutyDate: this.currentDay,
            roleId: this.selectRole,
            staffId: this.selectStaff
          }).then(this.createDutySucess)
        } else {
          this.$Message.error('Fail!')
        }
      })
    },
    createDutySucess (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('值班记录提交成功！')
        this.getAllDutyRecords()
      } else {
        this.$Message.error(res.msg)
      }
    },
    getAllDutyRecords () {
      axios.get('/back/dutyLists', {
        params: {
          departId: this.departSearch,
          dateStart: this.currentDay,
          dateEnd: this.currentDay
        }
      }).then(this.loadAllRelatedDuties)
    },
    loadAllRelatedDuties (response) {
      let res = response.data
      this.dutyLists = []
      if (res.code === 0) { // 返回正常
        if (this.departSearch !== '--') { // 本部门
          let data = res.data[0]
          let count = 0
          let num
          data.roleList.forEach((item, index) => {
            for (let i in item) {
              if (i === 'dutyList') {
                num = 0
                item[i].forEach((ite, ind) => { // 排班角色
                  this.dutyLists.push({
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
          // 对对象列表进行排序
          this.dutyLists.sort((obj1, obj2) => {
            if (obj1['departId'] === obj2['departId']) { // 部门相同
              if (obj1['roleId'] === obj2['roleId']) {
                return -1
              }
            }
          })
        }
      }
    },
    handleReset (name) {
      this.selectStaff = ''
      this.selectRole = ''
    },
    deleteDutyRecord (dutyId) {
      let that = this
      this.$Modal.confirm({
        title: '删除排班记录',
        content: '确认要删除该排班记录？',
        onOk: function () {
          axios.delete('/back/duty/' + dutyId).then(function (response) {
            if (response.data.code === 0) {
              that.getAllDutyRecords()
              that.$Message.success('删除成功！')
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    },
    getAllStaffSuccess (response) {
      let res = response.data
      if (res.code === 0) {
        res.data.forEach((item, index) => {
          this.staffLists.push({
            staffId: item.id,
            label: item.fullname
          })
        })
      }
    },
    getRelatedRoles (response) {
      let res = response.data
      if (res.code === 0) {
        res.data.forEach((item, index) => {
          this.roleLists.push({
            id: item.id,
            label: item.alias
          })
        })
      }
    },
    cancelModal () {
      this.bus.$emit('refreshCalendar')
      this.departOneModalCopy = false
    }
  },
  mounted () {
    this.selectRole = ''
    this.selectDepart = ''
    this.bus.$on('dayClickWatch', (param) => {
      this.departOneModalCopy = true
    })
    this.bus.$on('sendDepartData', (param) => {
      this.dutyLists = param
    })
    axios.get('/back/relations', {
      params: {
        fid: this.departSearch,
        genre: 1,
        not_add: 0
      }
    }).then(this.getAllStaffSuccess)
    axios.get('/back/relations', {
      params: {
        fid: this.departSearch,
        genre: 2,
        not_add: 0
      }
    }).then(this.getRelatedRoles)
  },
  updated () {
    //
  }
}
</script>

<style scoped lang="stylus">
  *
    box-sizing border-box
</style>
