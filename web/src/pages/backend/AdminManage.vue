<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">管理员列表</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createAdminFunc">新建</Button>
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
          <Input type="text" v-model="editFormValidate.adminName" placeholder="请输入用户名"></Input>
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
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AdminManage',
  data () {
    return {
      adminLists: [],
      createAdminFlag: false,
      editAdminFlag: false,
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
      curItem: {}
    }
  },
  methods: {
    loadAllAdmins (response) {
      let res = response.data
      if (res.code === 0) {
        this.adminLists = res.data
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
          axios.post('/back/admin', {
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
        axios.get('/back/admin').then(this.loadAllAdmins)
        this.createAdminFlag = false
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
          axios.put('/back/admin/' + this.curItem.id, {
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
        axios.get('/back/admin').then(this.loadAllAdmins)
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
          axios.delete('/back/admin/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('管理员删除成功！')
              axios.get('/back/admin').then(that.loadAllAdmins)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    }
  },
  mounted () {
    axios.get('/back/admin').then(this.loadAllAdmins)
  }
}
</script>

<style scoped>

</style>
