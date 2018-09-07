<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">用户管理</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small">新建</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="userLists"></Table>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserManage',
  data () {
    return {
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
            console.log(cssName)
            return h('div', [
              h('div', {
                props: {
                  className: cssName
                }
              }, '1')
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
          key: 'is_department'
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
              }, '编辑'),
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
              }, '删除')
            ])
          }
        }
      ],
      userLists: []
    }
  },
  mounted () {
    axios.get('/back/users').then(this.usersSuccFunc)
  },
  methods: {
    show (index) {
      this.$Modal.info({
        title: 'User Info',
        content: `Name：${this.data6[index].name}<br>Age：${this.data6[index].age}<br>Address：${this.data6[index].address}`
      })
    },
    remove (index) {
      this.data6.splice(index, 1)
    },
    usersSuccFunc (response) {
      let res = response.data
      if (res.code === 0) {
        this.userLists = res.data
      }
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
