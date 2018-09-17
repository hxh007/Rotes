<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">短信模板</h3>
      <Button :style="{'float': 'right'}" type="primary" size="small" @click="editTemplate">编辑</Button>
      <Icon type="md-help" @click="showDesc" :style="{'marginLeft': '10px', 'cursor': 'pointer'}" title="说明" />
    </div>
    <Modal
      v-model="descModalFlag"
      title="变量说明">
      <p>"{TOMORROW}"------该变量为程序的模板语法，切勿修改</p>
      <div slot="footer">
        <Button type="primary" size="large" @click="descriptionOk">确定</Button>
      </div>
    </Modal>
    <Divider/>
    <Table border :columns="columns" :data="templates"></Table>
    <!--编辑短信模板-->
    <Modal v-model="editFlag" title="编辑模板">
      <Form ref="editFormValidate" :model="editFormValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="模板内容" prop="temContent">
          <Input type="textarea" v-model="editFormValidate.tempContent" :autosize="{minRows: 3,maxRows: 8}" placeholder="请输入模板内容"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" size="large" @click="editSMSCancel('editFormValidate')">取消</Button>
        <Button type="primary" size="large" @click="editSMSOk('editFormValidate')">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'MessageManage',
  data () {
    return {
      templates: [],
      columns: [
        {
          title: '模板内容',
          key: 'tempContent'
        }
      ],
      editFlag: false,
      curItem: '',
      editFormValidate: {
        tempContent: ''
      },
      ruleValidate: {
        tempContent: [
          { required: true, message: '请输入模板内容', trigger: 'blur' }
        ]
      },
      descModalFlag: false
    }
  },
  methods: {
    loadAllTemplates (response) {
      this.templates = []
      let res = response.data
      if (res.code === 0) {
        this.templates.push(res.data)
      }
    },
    editTemplate () { // 编辑与新增
      this.curItem = this.templates[0].tempContent
      this.editFormValidate.tempContent = this.curItem
      this.editFlag = true
    },
    editSMSCancel (name) {
      this.editFlag = false
    },
    editSMSOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          axios.put('/back/tempContent', {
            tempContent: this.editFormValidate.tempContent
          }).then(this.editSMSSuccess)
        }
      })
      this.editFlag = false
    },
    editSMSSuccess (response) {
      let res = response.data
      if (res.code === 0) { // 修改成功
        this.$Message.success('修改成功！')
        axios.get('/back/tempContent').then(this.loadAllTemplates)
        this.editFlag = false
      } else {
        this.$Message.error(res.msg)
        this.editFlag = true
      }
    },
    descriptionOk () {
      this.descModalFlag = false
    },
    showDesc () {
      this.descModalFlag = true
    }
  },
  mounted () {
    axios.get('/back/tempContent').then(this.loadAllTemplates)
  }
}
</script>

<style scoped>

</style>
