<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">角色管理</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createRoleFunc">新建</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="roleLists"></Table>
    <!--创建角色modal-->
    <Modal v-model="createRoleFlag"
           title="新建角色">
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="角色名" prop="roleName">
          <Input type="text" v-model="formValidate.roleName" placeholder="请输入角色名"></Input>
        </FormItem>
        <FormItem label="角色别称" prop="roleAlias">
          <Input type="text" v-model="formValidate.roleAlias" placeholder="请输入角色别称"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="createRoleCancel('formValidate')">取消</Button>
        <Button type="primary" size="large" @click="createRoleOk('formValidate')">确定</Button>
      </div>
    </Modal>
    <!--编辑角色modal-->
    <Modal v-model="editRoleFlag"
           title="编辑角色">
      <Form ref="editFormValidate" :model="editFormValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="角色名" prop="roleName">
          <Input type="text" v-model="editFormValidate.roleName" placeholder="请输入角色名"></Input>
        </FormItem>
        <FormItem label="角色别称" prop="roleAlias">
          <Input type="text" v-model="editFormValidate.roleAlias" placeholder="请输入角色别称"></Input>
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
        <Button type="text" size="large" @click="editRoleCancel('editFormValidate')">取消</Button>
        <Button type="primary" size="large" @click="editRoleOk('editFormValidate')">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'RoleManage',
  data () {
    return {
      roleLists: [],
      createRoleFlag: false,
      editRoleFlag: false,
      columns: [
        {
          title: '角色名',
          key: 'name'
        },
        {
          title: '角色别称',
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
          title: '角色状态',
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
      curItem: {},
      formValidate: {
        roleName: '',
        roleAlias: ''
      },
      editFormValidate: {
        roleName: '',
        roleAlias: '',
        remark: ''
      },
      ruleValidate: {
        roleName: [
          { required: true, message: '请输入角色名', trigger: 'blur' }
        ],
        roleAlias: [
          { required: true, message: '请输入角色别称', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    loadAllRoles (response) {
      let res = response.data
      if (res.code === 0) {
        this.roleLists = res.data
      }
    },
    createRoleFunc () {
      this.createRoleFlag = true
    },
    createRoleCancel (name) {
      this.$refs[name].resetFields()
      this.createRoleFlag = false
    },
    createRoleOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.post(process.env.API_ROOT + '/auth/roles', {
            name: this.formValidate.roleName,
            alias: this.formValidate.roleAlias
          }).then(this.createRoleCallback)
        }
      })
    },
    createRoleCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('角色创建成功！')
        this.$refs.formValidate.resetFields()
        instance.get(process.env.API_ROOT + '/auth/roles').then(this.loadAllRoles)
        this.createRoleFlag = false
      } else {
        this.$Message.error(res.msg)
      }
    },
    show (params) {
      this.curItem = JSON.parse(JSON.stringify(params.row))
      this.editFormValidate.id = this.curItem.id
      this.editFormValidate.roleName = this.curItem.name
      this.editFormValidate.roleAlias = this.curItem.alias
      this.editFormValidate.remark = this.curItem.remark
      this.editFormValidate.status = this.curItem.status
      this.editRoleFlag = true
    },
    editRoleCancel (name) {
      this.$refs[name].resetFields()
      this.editRoleFlag = false
    },
    editRoleOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.put(process.env.API_ROOT + '/auth/roles/' + this.curItem.id, {
            name: this.editFormValidate.roleName,
            alias: this.editFormValidate.roleAlias,
            remark: this.editFormValidate.remark,
            status: this.editFormValidate.status
          }).then(this.editRoleCallback)
        }
      })
      // this.$refs[name].resetFields()
    },
    editRoleCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('角色编辑成功！')
        this.$refs.editFormValidate.resetFields()
        instance.get(process.env.API_ROOT + '/auth/roles').then(this.loadAllRoles)
        this.editRoleFlag = false
      } else {
        this.$Message.error(res.msg)
      }
    },
    remove (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除角色',
        content: '确认要删除该角色？',
        onOk: function () {
          instance.delete(process.env.API_ROOT + '/auth/roles/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('角色删除成功！')
              instance.get(process.env.API_ROOT + '/auth/roles').then(that.loadAllRoles)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    }
  },
  mounted () {
    instance.get(process.env.API_ROOT + '/auth/roles').then(this.loadAllRoles)
  }
}
</script>

<style scoped>

</style>
