<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">管理员列表</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createAdminFunc">新建</Button>
      <Button :style="{'float': 'right', 'marginRight': '10px'}" type="primary" size="small" @click="permissionManageFunc">权限管理</Button>
      <Button :style="{'float': 'right', 'marginRight': '10px'}" type="primary" size="small" @click="usersManageFunc">用户管理</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="adminLists"></Table>
    <!--创建管理员modal-->
    <Modal v-model="createAdminFlag"
           title="新建管理员">
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="用户名" prop="adminName">
          <Input type="text" v-model="formValidate.adminName" placeholder="请输入用户名"></Input>
        </FormItem>
        <FormItem label="昵称" prop="adminAlias">
          <Input type="text" v-model="formValidate.adminAlias" placeholder="请输入昵称"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="createAdminCancel('formValidate')">取消</Button>
        <Button type="primary" size="large" @click="createAdminOk('formValidate')">确定</Button>
      </div>
    </Modal>
    <!--编辑管理员modal-->
    <Modal v-model="editAdminFlag"
           title="编辑管理员">
      <Form ref="editFormValidate" :model="editFormValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="用户名" prop="adminName">
          <Input type="text" disabled v-model="editFormValidate.adminName" placeholder="请输入用户名"></Input>
        </FormItem>
        <FormItem label="昵称" prop="adminAlias">
          <Input type="text" v-model="editFormValidate.adminAlias" placeholder="请输入昵称"></Input>
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
        <Button type="text" size="large" @click="editAdminCancel('editFormValidate')">取消</Button>
        <Button type="primary" size="large" @click="editAdminOk('editFormValidate')">确定</Button>
      </div>
    </Modal>
    <!--管理组与权限-->
    <Modal v-model="permissionToGroupFlag" fullscreen title="管理组权限管理">
      <Row :style="{'marginTop': '20px'}">
        <Col span="18" offset="3">
          <div class="selectAdminGroup">
            <Row>
              <Col span="4">
                <h3>请选择管理组：</h3>
              </Col>
              <Col span="12">
                <Select v-model="selectAdminGroup" @on-change="loadGroupsPermissions">
                  <Option v-for="item in selectedGroups" :value="item.id" :key="item.id">{{ item.label }}</Option>
                </Select>
              </Col>
            </Row>
          </div>
          <div class="hasSelectedRoles">
            <h3>已有的权限列表</h3>
            <Table border height="500" :columns="hasSelectedCols" :data="hasSelectedAdminPermissions"></Table>
          </div>
          <Divider></Divider>
          <div class="couldSelectedRoles">
            <h3>可选择的权限列表</h3>
            <Table border height="500" :columns="couldSelectedCols" :data="couldSelectedAdminPermissions"></Table>
          </div>
        </Col>
      </Row>
    </Modal>
    <!--管理组与用户-->
    <Modal v-model="userToAdminGroupFlag" fullscreen title="管理组用户管理">
      <Row :style="{'marginTop': '20px'}">
      <Col span="18" offset="3">
        <div class="selectDepart">
          <Row>
            <Col span="4">
              <h3>请选择管理组：</h3>
            </Col>
            <Col span="12">
              <Select v-model="selectAdminGroup" @on-change="loadUsers">
                <Option v-for="item in selectedGroups" :value="item.id" :key="item.id">{{ item.label }}</Option>
              </Select>
            </Col>
          </Row>
        </div>
        <div class="hasSelectedRoles">
          <h3>已有的用户列表</h3>
          <Table height="300" border :columns="hasSelectedUserCols" :data="hasSelectedUsers"></Table>
        </div>
        <Divider></Divider>
        <div class="couldSelectedRoles">
          <h3>可选择用户列表</h3>
          <Table height="300" border :columns="couldSelectedUserCols" :data="couldSelectedUsers"></Table>
        </div>
      </Col>
    </Row>
    </Modal>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
import { loadLoginUserInfo, exitLogin } from '../../../libs/util'

export default {
  name: 'AdminManage',
  data () {
    return {
      adminLists: [],
      createAdminFlag: false,
      editAdminFlag: false,
      permissionToGroupFlag: false,
      userToAdminGroupFlag: false,
      columns: [
        {
          title: '用户名',
          key: 'name'
        },
        {
          title: '昵称',
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
          title: '状态',
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
          title: '操作',
          key: '操作',
          width: 150,
          align: 'center',
          render: (h, params) => {
            let cssName = 'normal'
            if (params.row.name === 'S_MANAGEMENT') { // 超级管理组
              cssName = 'noneStyle'
            }
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
                class: cssName,
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
        adminName: '',
        adminAlias: ''
      },
      ruleValidate: {
        adminName: [
          { required: true, message: '请输入用户名！', trigger: 'blur' }
        ],
        adminAlias: [
          { required: true, message: '请输入昵称！', trigger: 'blur' }
        ]
      },
      editFormValidate: {
        adminName: '',
        adminAlias: '',
        remark: ''
      },
      curItem: {},
      selectAdminGroup: '',
      selectedGroups: [],
      hasSelectedCols: [
        {
          title: '权限名',
          key: 'alias'
        },
        {
          title: '操作',
          key: '操作',
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
                    this.removePermissions(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      couldSelectedCols: [
        {
          title: '权限名',
          key: 'alias'
        },
        {
          title: '操作',
          key: '操作',
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
                    this.addPermission(params.row.id)
                  }
                }
              }, '添加')
            ])
          }
        }
      ],
      hasSelectedAdminPermissions: [],
      couldSelectedAdminPermissions: [],
      hasSelectedUsers: [],
      couldSelectedUsers: [],
      hasSelectedUserCols: [
        {
          title: '用户名',
          key: 'fullname'
        },
        {
          title: '操作',
          key: '操作',
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
                    this.removeUser(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      couldSelectedUserCols: [
        {
          title: '用户名',
          key: 'fullname'
        },
        {
          title: '操作',
          key: '操作',
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
                    this.addUser(params.row.id)
                  }
                }
              }, '添加')
            ])
          }
        }
      ],
      isEditGroup: 0 // 是否修改当前用户所在组 1---是 0---否
    }
  },
  methods: {
    loadAllAdmins (response) { // 生成可选的下拉菜单管理组
      let res = response.data
      if (res.code === 0) {
        this.adminLists = res.data
        this.adminLists.forEach((item, index) => {
          this.selectedGroups.push({
            label: item.alias,
            name: item.name,
            id: item.id
          })
        })
      }
    },
    createAdminFunc () {
      this.createAdminFlag = true
    },
    createAdminCancel (name) {
      this.$refs[name].resetFields()
      this.createAdminFlag = false
    },
    createAdminOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.post(process.env.API_ROOT + '/auth/managements', {
            name: this.formValidate.adminName,
            alias: this.formValidate.adminAlias
          }).then(this.createAdminCallback)
        }
      })
    },
    createAdminCallback (response) {
      let res = response.data
      if (res.code === 0) {
        // 创建成功
        this.$Message.success('管理员创建成功！')
        this.$refs.formValidate.resetFields()
        instance.get(process.env.API_ROOT + '/auth/managements').then(this.loadAllAdmins)
        this.createAdminFlag = false
      } else if (res.code === 2) { // 此时需要退出登录
        exitLogin()
        if (this.$route.path.indexOf('/backend') !== -1) {
          this.$router.push('/')
        }
      } else {
        this.$Message.error(res.msg)
      }
    },
    show (param) {
      this.curItem = JSON.parse(JSON.stringify(param.row))
      this.editFormValidate.id = this.curItem.id
      this.editFormValidate.adminName = this.curItem.name
      this.editFormValidate.adminAlias = this.curItem.alias
      this.editFormValidate.remark = this.curItem.remark
      this.editFormValidate.status = this.curItem.status
      this.editAdminFlag = true
    },
    editAdminCancel (name) {
      this.$refs[name].resetFields()
      this.editAdminFlag = false
    },
    editAdminOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.put(process.env.API_ROOT + '/auth/managements' + this.curItem.id, {
            name: this.editFormValidate.adminName,
            alias: this.editFormValidate.adminAlias,
            remark: this.editFormValidate.remark,
            status: this.editFormValidate.status
          }).then(this.editAdminSuccess)
        }
      })
    },
    editAdminSuccess (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('管理员信息编辑成功！')
        this.$refs.editFormValidate.resetFields()
        instance.get(process.env.API_ROOT + '/auth/managements').then(this.loadAllAdmins)
        this.editAdminFlag = false
      } else {
        this.editAdminFlag = true
      }
    },
    remove (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除管理员',
        content: '确认要删除该管理员？',
        onOk: function () {
          instance.delete(process.env.API_ROOT + '/auth/managements/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('管理员删除成功！')
              instance.get(process.env.API_ROOT + '/auth/managements').then(that.loadAllAdmins)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    },
    permissionManageFunc () {
      this.selectAdminGroup = ''
      this.hasSelectedAdminPermissions = []
      this.couldSelectedAdminPermissions = []
      this.permissionToGroupFlag = true
    },
    loadGroupsPermissions () {
      instance.get(process.env.API_ROOT + '/users/relations', { // 已添加关系
        params: {
          fid: this.selectAdminGroup,
          genre: 4,
          not_add: 0
        }
      }).then(this.loadAllHasSelectedPermissions)
      instance.get(process.env.API_ROOT + '/users/relations', { // 未添加关系
        params: {
          fid: this.selectAdminGroup,
          genre: 4,
          not_add: 1
        }
      }).then(this.loadAllCouldSelectedPermissions)
    },
    loadAllHasSelectedPermissions (response) {
      let res = response.data
      if (res.code === 0) {
        this.hasSelectedAdminPermissions = res.data
      }
    },
    loadAllCouldSelectedPermissions (response) {
      let res = response.data
      if (res.code === 0) {
        this.couldSelectedAdminPermissions = res.data
      }
    },
    addPermission (id) { // 添加权限给指定的管理组
      instance.post(process.env.API_ROOT + '/users/relations?fid=' + this.selectAdminGroup + '&genre=' + 4, {
        sid: id
      }).then(this.addPermissionSuccess)
    },
    addPermissionSuccess (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('权限添加成功！')
        this.loadGroupsPermissions()
      } else {
        this.$Message.error(res.msg)
      }
    },
    removePermissions (id) { // 删除已添加的用户
      instance.delete(process.env.API_ROOT + '/users/relations?fid=' + this.selectAdminGroup + '&genre=' + 4, {
        data: {
          sid: id
        }
      }).then(this.removePermissionSuccess)
    },
    removePermissionSuccess (response) {
      let res = response.data
      if (res.code === 0) { // 删除成功
        this.$Message.success('权限删除成功！')
        this.loadGroupsPermissions()
      } else {
        this.$Message.error(res.msg)
      }
    },
    usersManageFunc () {
      this.selectAdminGroup = ''
      this.hasSelectedUsers = []
      this.couldSelectedUsers = []
      this.userToAdminGroupFlag = true
    },
    loadUsers () {
      instance.get(process.env.API_ROOT + '/users/relations', { // 已添加关系
        params: {
          fid: this.selectAdminGroup,
          genre: 3,
          not_add: 0
        }
      }).then(this.loadAllHasSelectedUsers)
      instance.get(process.env.API_ROOT + '/users/relations', { // 未添加关系
        params: {
          fid: this.selectAdminGroup,
          genre: 3,
          not_add: 1
        }
      }).then(this.loadAllCouldSelectedUsers)
    },
    loadAllHasSelectedUsers (response) {
      let res = response.data
      if (res.code === 0) {
        this.hasSelectedUsers = res.data
      }
    },
    loadAllCouldSelectedUsers (response) {
      let res = response.data
      if (res.code === 0) {
        this.couldSelectedUsers = res.data
      }
    },
    addUser (id) { // 添加用户给指定管理组
      if (this.$store.state.currentUserId === id) this.isEditGroup = 1
      else this.isEditGroup = 0
      instance.post(process.env.API_ROOT + '/users/relations?fid=' + this.selectAdminGroup + '&genre=' + 3, {
        sid: id
      }).then(this.addUserSuccess)
    },
    addUserSuccess (response) {
      let res = response.data
      if (res.code === 0) {
        if (this.isEditGroup === 1) { // 修改当前登录用户所在的组
          loadLoginUserInfo()
        }
        this.$Message.success('添加成功！')
        this.loadUsers()
      } else {
        this.$Message.error(res.msg)
      }
    },
    removeUser (id) { // 删除已添加的用户
      if (this.$store.state.currentUserId === id) this.isEditGroup = 1
      else this.isEditGroup = 0
      instance.delete(process.env.API_ROOT + '/users/relations?fid=' + this.selectAdminGroup + '&genre=' + 3, {
        data: {
          sid: id
        }
      }).then(this.removeUserSuccess)
    },
    removeUserSuccess (response) {
      let res = response.data
      if (res.code === 0) { // 删除成功
        if (this.isEditGroup === 1) { // 修改当前登录用户所在的组
          loadLoginUserInfo()
        }
        this.$Message.success('删除成功！')
        this.loadUsers()
      } else {
        this.$Message.error(res.msg)
      }
    }
  },
  mounted () {
    instance.get(process.env.API_ROOT + '/auth/managements').then(this.loadAllAdmins)
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
