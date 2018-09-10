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
        :title="editFlag?'编辑用户':'新建用户'"
        @on-ok="createUserOk('formValidate')"
        @on-cancel="createUserCancel('formValidate')">
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
          <FormItem label="工号" prop="tagName" v-if="!editFlag">
            <Input type="text" v-model="formValidate.tagName" placeholder="请输入工号"></Input>
          </FormItem>
          <FormItem label="工号" prop="tagName" v-else>
            <Input type="text" v-model="curItem.tag" placeholder="请输入工号"></Input>
          </FormItem>
          <FormItem label="用户名" prop="userName" v-if="!editFlag">
            <Input type="text" v-model="formValidate.userName" placeholder="请输入用户名"></Input>
          </FormItem>
          <FormItem label="用户名" prop="userName" v-else>
            <Input type="text" v-model="curItem.username" placeholder="请输入用户名"></Input>
          </FormItem>
          <FormItem label="姓名" prop="fullName" v-if="!editFlag">
            <Input type="text" v-model="formValidate.fullName" placeholder="请输入姓名"></Input>
          </FormItem>
          <FormItem label="姓名" prop="fullName" v-else>
            <Input type="text" v-model="curItem.fullname" placeholder="请输入姓名"></Input>
          </FormItem>
          <FormItem label="手机号" prop="mobile" v-if="!editFlag">
            <Input type="text" v-model="formValidate.mobile" placeholder="请输入手机号"></Input>
          </FormItem>
          <FormItem label="手机号" prop="mobile" v-else>
            <Input type="text" v-model="curItem.mobile" placeholder="请输入手机号"></Input>
          </FormItem>
          <FormItem label="密码" prop="password" v-if="!editFlag">
            <Input type="password" v-model="formValidate.password" placeholder="请输入密码"></Input>
          </FormItem>
          <FormItem label="密码" prop="password" v-else>
            <Input type="password" v-model="curItem.password" placeholder="请输入密码"></Input>
          </FormItem>
        </Form>
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
            let manager = params.row.is_department === true ? '是' : '不是'
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
      formValidate: {
        tagName: '',
        userName: '',
        fullName: '',
        mobile: '',
        password: ''
      },
      ruleValidate: {
        userName: [{
          required: true, trigger: 'blur'
        }],
        fullName: [
          {required: true, trigger: 'blur'}
        ],
        mobile: [
          {required: true, trigger: 'blur'}
        ],
        password: [
          {required: true, type: 'string', trigger: 'blur'}
        ]
      }
    }
  },
  mounted () {
    axios.get('/back/users').then(this.usersSuccFunc)
  },
  methods: {
    show (params) {
      this.curItem = params.row
      this.createFlag = true // 打开modal框 与 create共用一个modal
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
      let url = !this.editFlag ? '/back/users' : '/back/users/' + this.curItem.id
      this.$refs[name].validate((valid) => {
        if (valid) {
          if (!this.editFlag) { // 创建
            axios.post(url, paramObj).then(this.createUserCallback)
          } else { // 编辑
            axios.put(url, paramObj).then(this.createUserCallback)
          }
        } else {
          this.$Message.error('Fail!')
        }
        this.$refs[name].resetFields()
      })
    },
    createUserCancel (name) { // 所有的取消回调
      this.$refs[name].resetFields()
      this.editFlag = this.editFlag === true ? false : this.editFlag
      this.curItem = {}
    },
    createUserCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('操作成功!')
      } else {
        this.$Message.error(res.msg + '!')
      }
      axios.get('/back/users').then(this.usersSuccFunc)
    }
  }
}
</script>

<style scoped lang="stylus">
.greenDot
  width 10px
  height 10px
  border-radius 50%
  background green
</style>
