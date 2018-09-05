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
          <Table border :columns="columns7" :data="data6" :height="440"></Table>
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
                  <Option value="刘梦溪">刘梦溪</Option>
                </Select>
              </FormItem>
              <FormItem>
                <Button type="primary" @click="handleSubmit('formValidate')">Submit</Button>
                <Button @click="handleReset('formValidate')" style="margin-left: 8px">Reset</Button>
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
      departOneModalCopy: false,
      columns7: [
        {
          title: '部门',
          key: 'departName',
          render: (h, params) => {
            return h('div', [
              h('strong', params.row.name)
            ])
          }
        },
        {
          title: 'Age',
          key: 'age'
        },
        {
          title: 'Address',
          key: 'address'
        },
        {
          title: 'Action',
          key: 'action',
          width: 150,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.show(params.index)
                  }
                }
              }, 'View'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.remove(params.index)
                  }
                }
              }, 'Delete')
            ])
          }
        }
      ],
      data6: [
        {
          name: 'John Brown',
          age: 18,
          address: 'New York No. 1 Lake Park'
        },
        {
          name: 'Jim Green',
          age: 24,
          address: 'London No. 1 Lake Park'
        },
        {
          name: 'Joe Black',
          age: 30,
          address: 'Sydney No. 1 Lake Park'
        },
        {
          name: 'Jon Snow',
          age: 26,
          address: 'Ottawa No. 2 Lake Park'
        }
      ]
    }
  },
  props: {
    departOneModal: Boolean,
    currentDay: String
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
    }
  },
  mounted () {
    this.bus.$on('dayClickWatch', (param) => {
      this.departOneModalCopy = true
      console.log(this.departOneModal)
    })
  }
}
</script>

<style scoped>

</style>
