<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden', verticalAlign: 'bottom', float: 'left', marginBottom: '10px'}">
      <router-link to="/backend/planTaskManage" :style="{float: 'left', fontSize: '18px', marginRight: '10px'}">
        <Icon type="md-arrow-back" :style="{color: '#5cadff'}" />
        <a>定时任务</a>
      </router-link>
      <h3 :style="{fontSize: '16px', 'float': 'left', borderLeft: '1px solid #666', paddingTop: '1px', paddingLeft: '10px'}">创建定时任务</h3>
    </div>
    <Divider/>
    <div class="timing-task">
      <h3>基本信息</h3>
      <Row :style="{marginTop: '20px', marginLeft: '10px', marginBottom: '10px'}">
        <Col span="12" offset="1">
          <Form ref="forItem" :rules="ruleValidate" :model="formItem" :label-width="80">
            <FormItem label="任务名称" prop="task">
              <Input v-model="formItem.task" placeholder="任务名称"></Input>
            </FormItem>
            <FormItem label="工具" prop="selectedFunc">
              <Select v-model="formItem.selectedFunc">
                <Option v-for="(item, key) in formItem.funcs" :value="item.func" :key="key">{{item.info}}</Option>
              </Select>
            </FormItem>
            <FormItem label="执行时间" prop="task">
              <Input v-model="formItem.time">
                <span slot="append" :style="{cursor: 'pointer'}" @click="selectTimeRule">选择时间规则</span>
              </Input>
            </FormItem>
          </Form>
        </Col>
      </Row>
      <h3>参数</h3>
      <Row>
        <Col offset="2">
          该工具无参数，请直接执行
        </Col>
      </Row>
      <Divider/>
      <Button type="primary">提交</Button>
    </div>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'CreateTimingTask',
  data () {
    return {
      formItem: {
        task: '',
        funcs: [],
        time: '',
        selectedFunc: ''
      },
      ruleValidate: {
        task: [
          { required: true, message: '任务名称！', trigger: 'blur' }
        ],
        selectedFunc: [
          { required: true, message: '请选择! ', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    loadFuncsCallback (response) {
      let res = response.data
      if (res.ret === 0) { // 获取数据成功
        this.formItem.funcs = res.detail
      } else { //  报错
        this.$Message.error('请求出错!')
      }
    },
    selectTimeRule () {
    }
  },
  mounted () {
    // 渲染工具参数
    instance.get('/back/cron/funcs').then(this.loadFuncsCallback)
  }
}
</script>

<style scoped lang="stylus">
.timing-task
  margin-top 50px
</style>
