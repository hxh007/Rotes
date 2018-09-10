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
              <div class="ivu-table-body ivu-table-overflowY" style="height: 100%">
                <table cellspacing="0" cellpadding="0" border="0" style="width: 663px">
                  <colgroup>
                    <col width="200">
                    <col width="200">
                    <col width="200">
                    <col width="72">
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
              <FormItem label="排班角色" prop="role">
                <Select v-model="formValidate.role" placeholder="选择排班角色">
                  <Option value="一线">一线</Option>
                  <Option value="二线">二线</Option>
                  <Option value="2.5线">2.5线</Option>
                </Select>
              </FormItem>
              <FormItem label="选择人员" prop="staff">
                <Select v-model="formValidate.staff" placeholder="选择排班人员">
                  <Option value="侯相会">侯相会</Option>
                  <Option value="张可">张可</Option>
                  <Option value="刘梦溪">刘孟希</Option>
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
  </Modal>
</template>

<script>
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
        role: [
          { required: true, message: '排班角色不能为空！', trigger: 'change' }
        ],
        staff: [
          { required: true, message: '排班人员不能为空！', trigger: 'change' }
        ]
      },
      departOneModalCopy: false
    }
  },
  props: {
    departOneModal: Boolean,
    currentDay: String,
    tableList: Array
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$Message.success('Success!')
        } else {
          this.$Message.error('Fail!')
        }
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    deleteDutyRecord (dutyId) {
      alert(dutyId)
    }
  },
  mounted () {
    this.bus.$on('dayClickWatch', (param) => {
      this.departOneModalCopy = true
    })
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
