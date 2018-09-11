<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">用户管理</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createUserFunc">新建</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="userLists"></Table>
    <Modal :style="{paddingRight: '10px'}"
        v-model="createFlag"
        title="新建用户">
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
          <FormItem label="工号" prop="tagName">
            <Input type="text" v-model="formValidate.tagName" placeholder="请输入工号"></Input>
          </FormItem>
          <FormItem label="用户名" prop="userName">
            <Input type="text" v-model="formValidate.userName" placeholder="请输入用户名"></Input>
          </FormItem>
          <FormItem label="姓名" prop="fullName">
            <Input type="text" v-model="formValidate.fullName" placeholder="请输入姓名"></Input>
          </FormItem>
          <FormItem label="手机号" prop="mobile">
            <Input type="text" v-model="formValidate.mobile" placeholder="请输入手机号"></Input>
          </FormItem>
          <FormItem label="密码" prop="password">
            <Input type="password" v-model="formValidate.password" placeholder="请输入密码"></Input>
          </FormItem>
          <FormItem label="确认密码" prop="confirmPassword">
            <Input type="password" v-model="formValidate.confirmPassword" placeholder="再次输入密码"></Input>
          </FormItem>
        </Form>
        <div slot="footer">
          <Button type="text" size="large" @click="createUserCancel('formValidate')">取消</Button>
          <Button type="primary" size="large" @click="createUserOk('formValidate')">确定</Button>
        </div>
      </Modal>
    <Modal :style="{paddingRight: '10px'}" v-model="editFlag" title="编辑用户">
      <Form ref="editFormValidate" :model="editFormValidate" :rules="isEditPass ? editRule1Validate : editRule2Validate" :label-width="80">
        <FormItem label="工号" prop="tagName">
          <Input type="text" v-model="editFormValidate.tagName" placeholder="请输入工号"></Input>
        </FormItem>
        <FormItem label="用户名" prop="userName">
          <Input type="text" v-model="editFormValidate.userName" placeholder="请输入用户名"></Input>
        </FormItem>
        <FormItem label="姓名" prop="fullName">
          <Input type="text" v-model="editFormValidate.fullName" placeholder="请输入姓名"></Input>
        </FormItem>
        <FormItem label="手机号" prop="mobile">
          <Input type="text" v-model="editFormValidate.mobile" placeholder="请输入手机号"></Input>
        </FormItem>
        <FormItem label="备注" prop="remark">
          <Input type="textarea" v-model="editFormValidate.remark" :autosize="true" placeholder="请输入备注" />
        </FormItem>
        <FormItem label="部门负责人">
          <i-switch v-model="editFormValidate.is_department">
            <span slot="open">是</span>
            <span slot="close">否</span>
          </i-switch>
        </FormItem>
        <FormItem label="用户状态">
          <i-switch v-model="editFormValidate.status" size="large">
            <span slot="open">激活</span>
            <span slot="close">禁用</span>
          </i-switch>
        </FormItem>
        <Divider/>
        <FormItem label="密码修改">
          <i-switch v-model="isEditPassword">
            <span slot="open">开</span>
            <span slot="close">关</span>
          </i-switch>
        </FormItem>
        <FormItem label="密码" prop="password">
          <Input type="password" :disabled="!isEditPassword" v-model="editFormValidate.password" placeholder="请输入密码"></Input>
        </FormItem>
        <FormItem label="确认密码" prop="confirmPassword">
          <Input type="password" :disabled="!isEditPassword" v-model="editFormValidate.confirmPassword" placeholder="再次输入密码"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="editUserCancel('editFormValidate')">取消</Button>
        <Button type="primary" size="large" @click="editUserOk('editFormValidate')">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserManage',
  data () {
    return {
      createFlag: false,
      editFlag: false,
      curItem: {},
      columns: [
        {
          title: '工号',
          key: 'tag',
          render: (h, params) => {
            let tag = params.row.tag
            if (!params.row.tag) { // 为空
              tag = '--'
            }
            return h('div', [
              h('div', tag)
            ])
          },
          sortable: true
        },
        {
          title: '用户名',
          key: 'username'
        },
        {
          title: '姓名',
          key: 'fullname'
        },
        {
          title: '手机号',
          key: 'mobile'
        },
        {
          title: '用户状态',
          key: 'status',
          render: (h, params) => {
            let cssName = params.row.status === true ? 'greenDot' : 'redDot'
            return h('div', [
              h('div', {
                class: cssName,
                style: {
                }
              })
            ])
          }
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
          title: '部门负责人',
          key: 'is_department',
          render: (h, params) => {
            let manager = params.row.is_department === true ? '是' : '否'
            return h('div', {}, manager)
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
      userLists: [],
      isEditPassword: false,
      formValidate: {
        tagName: '',
        userName: '',
        fullName: '',
        mobile: '',
        password: '',
        confirmPassword: ''
      },
      ruleValidate: {
        userName: [{
          required: true, message: '请输入用户名!', trigger: 'blur'
        }],
        fullName: [
          {required: true, message: '请输入姓名!', trigger: 'blur'}
        ],
        mobile: [
          {required: true, message: '请输入手机号码!', trigger: 'blur'}
        ],
        password: [
          {required: true, type: 'string', message: '请输入密码!', trigger: 'blur'}
        ],
        confirmPassword: [
          {
            required: true,
            type: 'string',
            trigger: 'blur',
            validator: this.validatorCreateUser
          }
        ]
      },
      editFormValidate: {
        tagName: '',
        userName: '',
        fullName: '',
        mobile: '',
        remark: '',
        password: '',
        confirmPassword: ''
      },
      editRule1Validate: {
        userName: [{
          required: true, message: '请输入用户名!', trigger: 'blur'
        }],
        fullName: [
          {required: true, message: '请输入姓名!', trigger: 'blur'}
        ],
        mobile: [
          {required: true, message: '请输入手机号码!', trigger: 'blur'}
        ],
        password: [
          {required: this.isEditPass, type: 'string', message: '请输入密码!', trigger: 'blur'}
        ],
        confirmPassword: [
          {
            required: this.isEditPass,
            type: 'string',
            trigger: 'blur',
            validator: this.validatorEditUser
          }
        ]
      },
      editRule2Validate: {
        userName: [{
          required: true, message: '请输入用户名!', trigger: 'blur'
        }],
        fullName: [
          {required: true, message: '请输入姓名!', trigger: 'blur'}
        ],
        mobile: [
          {required: true, message: '请输入手机号码!', trigger: 'blur'}
        ]
      }
    }
  },
  computed: {
    isEditPass () {
      return this.isEditPassword
    }
  },
  mounted () {
    axios.get('/back/users').then(this.usersSuccFunc)
  },
  methods: {
    show (params) {
      this.curItem = params.row
      let obj = JSON.parse(JSON.stringify(this.curItem))
      this.editFormValidate.tagName = obj.tag
      this.editFormValidate.userName = obj.username
      this.editFormValidate.fullName = obj.fullname
      this.editFormValidate.remark = obj.remark
      this.editFormValidate.mobile = obj.mobile
      this.editFormValidate.is_department = obj.is_department
      this.editFormValidate.status = obj.status
      this.editFlag = true
    },
    remove (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除用户',
        content: '确认要删除该用户？',
        onOk: function () {
          axios.delete('/back/users/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('数据删除成功！')
              axios.get('/back/users').then(that.usersSuccFunc)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    },
    usersSuccFunc (response) {
      let res = response.data
      if (res.code === 0) {
        this.userLists = res.data
      }
    },
    createUserFunc () {
      this.createFlag = true
    },
    createUserOk (name) {
      let paramObj = {
        tag: this.formValidate.tagName,
        username: this.formValidate.userName,
        fullname: this.formValidate.fullName,
        mobile: this.formValidate.mobile,
        password: this.formValidate.password
      }
      this.$refs[name].validate((valid) => {
        if (valid) {
          axios.post('/back/users', paramObj).then(this.createUserCallback)
          this.createFlag = false
        } else {
          this.$Message.error('Fail!')
        }
        this.$refs[name].resetFields()
      })
    },
    editUserOk (name) {
      let paramObj = {
        tag: this.editFormValidate.tagName,
        username: this.editFormValidate.userName,
        fullname: this.editFormValidate.fullName,
        mobile: this.editFormValidate.mobile,
        remark: this.editFormValidate.remark,
        is_department: this.editFormValidate.is_department,
        status: this.editFormValidate.status
      }
      if (this.isEditPass) { // 编辑密码
        paramObj.password = this.editFormValidate.password
      }
      console.log(paramObj)
      this.$refs[name].validate((valid) => {
        if (valid) { // 有效
          axios.put('/back/users/' + this.curItem.id, paramObj).then(this.editUserCallback)
        } else {
          this.$Message.error('修改失败！')
        }
      })
    },
    createUserCancel (name) { // 所有的取消回调
      this.$refs[name].resetFields()
      this.createFlag = false
    },
    editUserCancel (name) {
      this.$refs[name].resetFields()
      this.curItem = {}
      this.editFlag = false
    },
    createUserCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('创建用户成功!')
      } else {
        this.$Message.error(res.msg + '!')
      }
      axios.get('/back/users').then(this.usersSuccFunc)
    },
    editUserCallback (response) {
      let res = response.data
      if (res.code === 0) { // 数据提交成功
        this.$Message.success('用户修改成功！')
        this.editFlag = false
      } else {
        this.$Message.error(res.msg)
      }
      axios.get('/back/users').then(this.usersSuccFunc)
    },
    validatorCreateUser (rule, value, callback) {
      if (value === '') {
        callback(new Error('请再次输入密码！'))
      } else if (value !== this.formValidate.password) {
        callback(new Error('两次密码输入不一致!'))
      } else {
        callback()
      }
    },
    validatorEditUser (rule, value, callback) {
      if (value === '') {
        callback(new Error('请再次输入密码！'))
      } else if (value !== this.editFormValidate.password) {
        callback(new Error('两次密码输入不一致!'))
      } else {
        callback()
      }
    }
  }
}
</script>

<style scoped lang="stylus">
.ivu-modal-body
  overflow hidden
</style>
