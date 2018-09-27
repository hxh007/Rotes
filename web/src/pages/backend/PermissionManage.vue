<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">权限管理</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createPermissionFunc">新建</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="permissionLists"></Table>
    <!--创建权限modal-->
    <Modal v-model="createPermissionFlag"
           title="新建权限">
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="部门">
          <Select v-model="selectDepart">
            <Option v-for="item in departLists" :value="item.id" :key="item.id">{{ item.label }}</Option>
          </Select>
        </FormItem>
        <FormItem label="权限名">
          <Select v-model="selectAction">
            <Option v-for="item in actionLists" :value="item.value" :key="item.id">{{item.label}}</Option>
          </Select>
        </FormItem>
        <FormItem label="权限别称" prop="alias">
          <Input type="text" v-model="formValidate.alias" placeholder="请输入权限别称,格式：部门-操作"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="createPermissionCancel('formValidate')">取消</Button>
        <Button type="primary" size="large" @click="createPermissionOk('formValidate')">确定</Button>
      </div>
    </Modal>
    <!--编辑权限modal-->
    <Modal v-model="editPermissionFlag"
           title="编辑权限">
      <Form ref="editFormValidate" :model="editFormValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="部门">
          <Select v-model="selectDepart">
            <Option v-for="item in departLists" :value="item.id" :key="item.id">{{ item.label }}</Option>
          </Select>
        </FormItem>
        <FormItem label="权限名">
          <Select v-model="selectAction">
            <Option v-for="item in actionLists" :value="item.value" :key="item.id">{{item.label}}</Option>
          </Select>
        </FormItem>
        <FormItem label="权限别称" prop="alias">
          <Input type="text" v-model="editFormValidate.alias" placeholder="请输入权限别称,格式：部门-操作"></Input>
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
        <Button type="text" size="large" @click="editPermissionCancel('editFormValidate')">取消</Button>
        <Button type="primary" size="large" @click="editPermissionOk('editFormValidate')">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'PermissionManage',
  data () {
    return {
      columns: [
        {
          title: '权限',
          key: 'codename'
        },
        {
          title: '权限别称',
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
      permissionLists: [],
      departLists: [], // 可以最开始的时候加载出来
      actionLists: [],
      formValidate: {
        department: '',
        codeName: '',
        alias: ''
      },
      ruleValidate: {
        department: [
          { required: true, message: '请选择部门名', trigger: 'change' }
        ],
        codeName: [
          { required: true, message: '请选择权限名', trigger: 'change' }
        ],
        alias: [
          { required: true, message: '请输入权限别称,格式：部门-操作', trigger: 'blur' }
        ]
      },
      editFormValidate: {
        department: '',
        codeName: '',
        alias: '',
        remark: '',
        status: ''
      },
      createPermissionFlag: false,
      editPermissionFlag: false,
      selectDepart: '',
      selectAction: '',
      curItem: {}
    }
  },
  methods: {
    loadAllPermissions (response) {
      let res = response.data
      if (res.code === 0) {
        this.permissionLists = res.data
      }
    },
    createPermissionFunc () {
      this.selectDepart = ''
      this.selectAction = ''
      this.createPermissionFlag = true
    },
    createPermissionCancel (name) {
      this.$refs[name].resetFields()
      this.createPermissionFlag = false
    },
    createPermissionOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.post('/back/permissions', {
            derpartment_id: this.selectDepart,
            codename: this.selectAction,
            alias: this.formValidate.alias
          }).then(this.createPermissionCallback)
        }
      })
    },
    createPermissionCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('权限添加成功！')
        instance.get('/back/permissions').then(this.loadAllPermissions)
        this.createPermissionFlag = false
      } else {
        this.$Message.error(res.msg)
      }
    },
    show (params) {
      this.curItem = JSON.parse(JSON.stringify(params.row))
      this.editFormValidate.id = this.curItem.id
      this.selectAction = this.curItem.codename
      this.selectDepart = this.curItem.department_id
      this.editFormValidate.alias = this.curItem.alias
      this.editFormValidate.remark = this.curItem.remark
      this.editFormValidate.status = this.curItem.status
      this.editPermissionFlag = true
    },
    editPermissionCancel (name) {
      this.$refs[name].resetFields()
      this.editPermissionFlag = false
    },
    editPermissionOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.put('/back/permissions/' + this.editFormValidate.id, {
            department_id: this.selectDepart,
            codename: this.selectAction,
            alias: this.editFormValidate.alias,
            remark: this.editFormValidate.remark,
            status: this.editFormValidate.status
          }).then(this.editPermissionSuccess)
        }
      })
    },
    editPermissionSuccess (response) {
      let res = response.data
      if (res.code === 0) { // 编辑成功
        this.$Message.success('编辑成功！')
        this.$refs.editFormValidate.resetFields()
        instance.get('/back/permissions').then(this.loadAllPermissions)
        this.editPermissionFlag = false
      } else {
        this.$Message.error(res.msg)
        this.editPermissionFlag = true
      }
    },
    remove (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除权限',
        content: '确认要删除该权限？',
        onOk: function () {
          instance.delete('/back/permissions/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('权限删除成功！')
              instance.get('/back/permissions').then(that.loadAllPermissions)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    }
  },
  mounted () {
    let that = this
    instance.get('/back/permissions').then(this.loadAllPermissions)
    instance.get('/back/departments').then(function (response) {
      let res = response.data
      if (res.code === 0) { // 查询成功
        res.data.forEach(function (item, index) {
          that.departLists.push({
            label: item.alias,
            name: item.name,
            id: item.id
          })
        })
      }
    })
    instance.get('/back/actiontypes').then(function (response) {
      let res = response.data
      if (res.code === 0) {
        res.data.forEach(function (item, index) {
          that.actionLists.push({
            id: item.id,
            value: item.codename,
            label: item.alias
          })
        })
      }
    })
  }
}
</script>

<style scoped lang="stylus">

</style>
