<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">操作管理</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="createOperationFunc">新建</Button>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="opertionLists"></Table>
    <!--创建操作modal-->
    <Modal v-model="createOperationFlag"
           title="新建部门">
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="操作名" prop="operationName">
          <Input type="text" v-model="formValidate.operationName" placeholder="请输入操作名"></Input>
        </FormItem>
        <FormItem label="操作别称" prop="operationAlias">
          <Input type="text" v-model="formValidate.operationAlias" placeholder="请输入操作别称"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="createOperationCancel('formValidate')">取消</Button>
        <Button type="primary" size="large" @click="createOperationOk('formValidate')">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'OperationManage',
  data () {
    return {
      opertionLists: [],
      columns: [
        {
          title: '操作名',
          key: 'codename'
        },
        {
          title: '操作别称',
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
                    this.remove(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      createOperationFlag: false,
      formValidate: {
        operationName: '',
        operationAlias: ''
      },
      ruleValidate: {
        operationName: [
          { required: true, message: '请输入操作名称！', trigger: 'blur' }
        ],
        operationAlias: [
          { required: true, message: '请输入操作别称！', trigger: 'blur' }
        ]
      },
      curItem: {}
    }
  },
  methods: {
    createOperationFunc () {
      this.createOperationFlag = true
    },
    getAllOperations (response) {
      let res = response.data
      if (res.code === 0) {
        this.opertionLists = res.data
      }
    },
    createOperationCancel (name) {
      this.$refs[name].resetFields()
      this.createOperationFlag = false
    },
    createOperationOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          instance.post('/back/actiontypes', {
            codename: this.formValidate.operationName,
            alias: this.formValidate.operationAlias
          }).then(this.createOperationCallback)
        }
      })
    },
    createOperationCallback (response) {
      let res = response.data
      if (res.code === 0) {
        this.$Message.success('操作创建成功！')
        this.$refs.formValidate.resetFields()
        this.createOperationFlag = false
        instance.get('/back/actiontypes').then(this.getAllOperations)
      }
    },
    remove (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除操作',
        content: '确认要删除该操作？',
        onOk: function () {
          instance.delete('/back/actiontypes/' + id).then(function (response) {
            if (response.data.code === 0) {
              that.$Message.success('操作删除成功！')
              instance.get('/back/actiontypes').then(that.getAllOperations)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    }
  },
  mounted () {
    instance.get('/back/actiontypes').then(this.getAllOperations)
  }
}
</script>

<style scoped>

</style>
