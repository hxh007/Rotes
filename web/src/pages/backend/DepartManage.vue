<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">部门管理</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createDepartFunc">新建</Button>
      <Button :style="{'float': 'right', 'marginRight': '10px'}" type="primary" size="small" @click="roleManageFunc">角色管理</Button>
      <Button :style="{'float': 'right', 'marginRight': '10px'}" type="primary" size="small" @click="usersManageFunc">用户管理</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="departLists"></Table>
    <!--创建部门modal-->
    <Modal v-model="createDepartFlag"
           title="新建部门">
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="部门名" prop="departName">
          <Input type="text" v-model="formValidate.departName" placeholder="请输入部门名"></Input>
        </FormItem>
        <FormItem label="部门别称" prop="departAlias">
          <Input type="text" v-model="formValidate.departAlias" placeholder="请输入部门别称"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="createDepartCancel('formValidate')">取消</Button>
        <Button type="primary" size="large" @click="createDepartOk('formValidate')">确定</Button>
      </div>
    </Modal>
    <!--编辑部门modal-->
    <Modal v-model="editDepartFlag"
           title="编辑部门">
      <Form ref="editFormValidate" :model="editFormValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="部门名" prop="departName">
          <Input type="text" v-model="editFormValidate.departName" placeholder="请输入部门名"></Input>
        </FormItem>
        <FormItem label="部门别称" prop="departAlias">
          <Input type="text" v-model="editFormValidate.departAlias" placeholder="请输入部门别称"></Input>
        </FormItem>
        <FormItem label="备注" prop="remark">
          <Input type="textarea" v-model="editFormValidate.remark" :autosize="true" placeholder="请输入备注" />
        </FormItem>
        <FormItem label="状态">
          <i-switch v-model="editFormValidate.status" size="large">
            <span slot="open">激活</span>
            <span slot="close">禁用</span>
          </i-switch>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="editDepartCancel('editFormValidate')">取消</Button>
        <Button type="primary" size="large" @click="editDepartOk('editFormValidate')">确定</Button>
      </div>
    </Modal>
    <!--编辑部门的角色-->
    <Modal v-model="roleToDepartFlag" fullscreen title="部门角色管理">
      <Row :style="{'marginTop': '20px'}">
        <Col span="18" offset="3">
          <div class="selectDepart">
            <Row>
              <Col span="4">
                <h3>请选择部门：</h3>
              </Col>
              <Col span="12">
                <Select v-model="selectDepart" @on-change="loadRoles">
                  <Option v-for="item in selectedDeparts" :value="item.id" :key="item.id">{{ item.label }}</Option>
                </Select>
              </Col>
            </Row>
          </div>
          <div class="hasSelectedRoles">
            <h3>已有的角色列表</h3>
            <Table border :columns="hasSelectedCols" :data="hasSelectedRoles"></Table>
          </div>
          <Divider></Divider>
          <div class="couldSelectedRoles">
            <h3>可选择角色列表</h3>
            <Table border :columns="couldSelectedCols" :data="couldSelectedRoles"></Table>
          </div>
        </Col>
      </Row>
    </Modal>
    <!--编辑部门的用户-->
    <Modal v-model="userToDepartFlag" fullscreen title="部门用户管理">
      <Row :style="{'marginTop': '20px'}">
        <Col span="18" offset="3">
          <div class="selectDepart">
            <Row>
              <Col span="4">
                <h3>请选择部门：</h3>
              </Col>
              <Col span="12">
                <Select v-model="selectDepart" @on-change="loadRoles">
                  <Option v-for="item in selectedDeparts" :value="item.id" :key="item.id">{{ item.label }}</Option>
                </Select>
              </Col>
            </Row>
          </div>
          <div class="hasSelectedRoles">
            <h3>已有的用户列表</h3>
            <Table border :columns="hasSelectedUserCols" :data="hasSelectedUsers"></Table>
          </div>
          <Divider></Divider>
          <div class="couldSelectedRoles">
            <h3>可选择用户列表</h3>
            <Table border :columns="couldSelectedUserCols" :data="couldSelectedUsers"></Table>
          </div>
        </Col>
      </Row>
    </Modal>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'DepartManage',
  data () {
    return {
      model9: '',
      departLists: [],
      selectedDeparts: [],
      createDepartFlag: false,
      editDepartFlag: false,
      roleToDepartFlag: false,
      userToDepartFlag: false,
      columns: [
        {
          title: '部门名',
          key: 'name'
        },
        {
          title: '部门别称',
          key: 'alias'
        },
        {
          title: '备注',
          key: 'remark',
          render: (h, params) => {
            let remark = params.row.remark
            if (!params.row.remark) { // 为空
              remark = '--'
            }
            return h('div', {
              props: {}
            }, remark)
          }
        },
        {
          title: '权限状态',
          key: 'status',
          render: (h, params) => {
            let cssName = params.row.status === true ? 'greenDot' : 'redDot'
            return h('div', [
              h('div', {
                class: cssName
              })
            ])
          }
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
                    this.show(params)
                  }
                }
              }, '编辑'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.remove(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      formValidate: {
        departName: '',
        departAlias: ''
      },
      ruleValidate: {
        departName: [
          { required: true, message: '请输入部门名', trigger: 'blur' }
        ],
        departAlias: [
          { required: true, message: '请输入部门别称', trigger: 'blur' }
        ]
      },
      editFormValidate: {
        departName: '',
        departAlias: '',
        remark: ''
      },
      curItem: {},
      selectDepart: '',
      hasSelectedCols: [
        {
          title: '角色名',
          key: 'alias'
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
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.removeRole(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      couldSelectedCols: [
        {
          title: '角色名',
          key: 'alias'
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
                on: {
                  click: () => {
                    this.addRole(params.row.id)
                  }
                }
              }, '添加')
            ])
          }
        }
      ],
      hasSelectedUserCols: [],
      couldSelectedUserCols: [],
      hasSelectedRoles: [],
      couldSelectedRoles: [],
      hasSelectedUsers: [],
      couldSelectedUsers: []
    }
  },
  methods: {
    loadAllDeparts (response) {
      let res = response.data
      if (res.code === 0) {
        this.departLists = res.data
      }
      this.departLists.forEach((item, index) => {
        this.selectedDeparts.push({
          label: item.alias,
          name: item.name,
          id: item.id
        })
      })
    },
    createDepartFunc () {
      this.createDepartFlag = true
    },
    createDepartCancel (name) {
      this.createDepartFlag = false
      this.$refs[name].resetFields()
    },
    createDepartOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          axios.post('/back/departments', {
            name: this.formValidate.departName,
            alias: this.formValidate.departAlias
          }).then(this.createDepartCallback)
        }
      })
    },
    createDepartCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('部门创建成功！')
        this.createDepartFlag = false
        this.$refs.formValidate.resetFields()
        axios.get('/back/departments').then(this.loadAllDeparts)
      }
    },
    editDepartCancel (name) {
      this.editDepartFlag = false
      this.$refs[name].resetFields()
    },
    editDepartOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          axios.put('/back/departments/' + this.editFormValidate.id, {
            name: this.editFormValidate.departName,
            alias: this.editFormValidate.departAlias,
            remark: this.editFormValidate.remark,
            status: this.editFormValidate.status
          }).then(this.editDepartCallback)
        } else {
          alert(0)
        }
      })
    },
    editDepartCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('部门信息编辑成功！')
        this.editDepartFlag = false
        axios.get('/back/departments').then(this.loadAllDeparts)
      } else {
        this.$Message.error('部门信息编辑失败！')
        this.editDepartFlag = true
      }
    },
    show (params) {
      this.curItem = JSON.parse(JSON.stringify(params.row))
      this.editFormValidate.id = this.curItem.id
      this.editFormValidate.departName = this.curItem.name
      this.editFormValidate.departAlias = this.curItem.alias
      this.editFormValidate.remark = this.curItem.remark
      this.editFormValidate.status = this.curItem.status
      this.editDepartFlag = true
    },
    remove (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除部门',
        content: '确认要删除该部门？',
        onOk: function () {
          axios.delete('/back/departments/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('部门删除成功！')
              axios.get('/back/departments').then(that.loadAllDeparts)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    },
    roleManageFunc () {
      this.roleToDepartFlag = true
    },
    loadRoles () {
      axios.get('/back/relations', { // 已添加关系
        params: {
          fid: this.selectDepart,
          genre: 2,
          not_add: 0
        }
      }).then(this.loadAllHasSelectedRoles)
      axios.get('/back/relations', { // 未添加关系
        params: {
          fid: this.selectDepart,
          genre: 2,
          not_add: 1
        }
      }).then(this.loadAllCouldSelectedRoles)
    },
    loadAllHasSelectedRoles (response) {
      let res = response.data
      if (res.code === 0) {
        this.hasSelectedRoles = res.data
      }
    },
    loadAllCouldSelectedRoles (response) {
      let res = response.data
      if (res.code === 0) {
        this.couldSelectedRoles = res.data
      }
    },
    removeRole (id) { // 删除已添加的角色
      axios.post('/back/relations', {
        fid: this.selectDepart,
        genre: 2,
        sid: id
      }).then(this.removeRoleSuccess)
    },
    removeRoleSuccess (response) {
      let res = response.data
      if (res.code === 0) { // 删除成功
        this.loadRoles()
      }
    },
    addRole (id) { // 添加角色给指定部门
      axios.post('/back/relations', {
        fid: this.selectDepart,
        genre: 2,
        sid: id
      }).then(this.addRoleSuccess)
    },
    addRoleSuccess (response) {
      let res = response.data
      if (res.code === 0) {
        this.loadRoles()
      }
    },
    usersManageFunc () {}
  },
  mounted () {
    axios.get('/back/departments').then(this.loadAllDeparts)
  }
}
</script>

<style scoped lang="stylus">
.hasSelectedRoles
  margin-top 30px
  h3
    margin-bottom 10px
.couldSelectedRoles
  margin-top 30px
  h3
    margin-bottom 10px
</style>
