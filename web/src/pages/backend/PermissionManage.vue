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
  </div>
</template>

<script>
import axios from 'axios'
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
        // department: '',
        // codeName: '',
        alias: ''
      },
      ruleValidate: {
        // department: [
        //   { required: true, message: '请选择部门名', trigger: 'change' }
        // ],
        // codeName: [
        //   { required: true, message: '请选择权限名', trigger: 'change' }
        // ],
        alias: [
          { required: true, message: '请输入权限别称,格式：部门-操作', trigger: 'blur' }
        ]
      },
      createPermissionFlag: false,
      editPermissionFlag: false,
      selectDepart: '',
      selectAction: ''
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
      this.createPermissionFlag = true
    },
    createPermissionCancel (name) {
      this.$refs[name].resetFields()
      this.createPermissionFlag = false
    },
    createPermissionOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          axios.post('/back/permissions', {
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
        axios.get('/back/permissions').then(this.loadAllPermissions)
        this.createPermissionFlag = false
      } else {
        this.$Message.error(res.msg)
      }
    }
  },
  mounted () {
    let that = this
    axios.get('/back/permissions').then(this.loadAllPermissions)
    axios.get('/back/departments').then(function (response) {
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
    axios.get('/back/actiontypes').then(function (response) {
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
