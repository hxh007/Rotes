<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">定时任务</h3>
      <div :style="{'float': 'right', 'marginLeft': '10px'}">
        <Dropdown @on-click="operateOptions">
          <a href="javascript:void(0)">
            操作
            <Icon type="ios-arrow-down"></Icon>
          </a>
          <DropdownMenu slot="list">
            <DropdownItem name="edit">编辑</DropdownItem>
          </DropdownMenu>
        </Dropdown>
        <Button :type="scheduler_flag" size="small">调度器：{{scheduler_text}}</Button>
        <Drawer title="调度器" :closable="false" v-model="value1">
          <Form :model="formItem" :label-width="80">
            <FormItem label="时区">
              <Input disabled v-model="formItem.tz" :autosize="{minRows: 2,maxRows: 5}"></Input>
            </FormItem>
            <FormItem label="类型">
              <Input disabled v-model="formItem.type" :autosize="{minRows: 2,maxRows: 5}"></Input>
            </FormItem>
            <FormItem label="状态">
              <i-switch :disabled="disabled" v-model="formItem.status" size="large" @on-change="changeStatus">
                <span slot="open">运行</span>
                <span slot="close">暂停</span>
              </i-switch>
              <Button type="primary" @click="disabled = !disabled">Toggle Disabled</Button>
            </FormItem>
          </Form>
        </Drawer>
      </div>
      <router-link :style="{'float': 'left', 'marginLeft': '10px'}"  to="/backend/planTaskManage/createTimingTask" role="button">
        <Button type="primary" size="small">创建定时任务</Button>
      </router-link>
      <router-link :style="{'float': 'left', marginLeft: '10px'}" to="/backend/triggerActions">
        <Button type="primary" size="small">人工操作</Button>
      </router-link>
    </div>
    <Divider/>
    <Table border :columns="columns" :data="taskLists"></Table>
    <Modal
      v-model="singleFlag"
      title="获取单个定时任务">
      <Form :label-width="100">
        <FormItem label="工具">
          <h3>{{singleJob.func}}</h3>
        </FormItem>
        <FormItem label="触发器">
          <h3>{{singleJob.trigger}}</h3>
        </FormItem>
        <FormItem label="任务名称">
          <h3>{{singleJob.name}}</h3>
        </FormItem>
        <FormItem label="下次执行时间">
          <h3>
            <Time :time="singleJob.next_run" :interval="1"></Time>
          </h3>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="primary" @click="cancelSingleModal">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'PlanTaskManage',
  data () {
    return {
      value1: false,
      scheduler_flag: 'primary',
      scheduler_text: '运行中',
      formItem: {
        tz: '',
        type: '',
        status: ''
      },
      columns: [
        {
          title: '任务名',
          key: 'name'
        },
        {
          title: '任务类型',
          key: 'func'
        },
        {
          title: '下次执行时间',
          key: 'next_run',
          render: (h, params) => {
            let time
            if (params.row.next_run === null) {
              time = '--'
              return h('div', {}, time)
            } else {
              time = new Date(Date(params.row.next_run))
              return h('Time', {
                props: {
                  interval: 1,
                  time: time
                }
              }, time)
            }
          }
        },
        {
          title: '操作',
          key: '操作',
          width: 300,
          align: 'center',
          render: (h, params) => {
            let cssName = params.row.next_run === null ? 'noneStyle' : 'normal'
            return h('div', [
              h('Button', {
                props: {
                  type: 'warning',
                  size: 'small'
                },
                class: cssName,
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    // 暂停
                    if (params.row.next_run && params.row.next_run !== 'null') {
                      this.pauseJob(params.row.id)
                    }
                  }
                }
              }, '暂停'),
              h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                class: cssName === 'noneStyle' ? 'normal' : 'noneStyle',
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    // 恢复
                    this.recoverJob(params.row.id)
                  }
                }
              }, '恢复'),
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
                    // 获取
                    this.getSingleJob(params.row.id)
                  }
                }
              }, '获取'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.removeJob(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      taskLists: [],
      disabled: true,
      singleJob: {
        name: '',
        trigger: '',
        next_run: '',
        func: ''
      },
      singleFlag: false
    }
  },
  methods: {
    loadAllTasks (response) {
      let res = response.data
      this.taskLists = []
      if (res.detail.length > 0) {
        res.detail.forEach((item, index) => {
          this.taskLists.push({
            id: item.id,
            name: item.name,
            func: item.func,
            next_run: item.next_run
          })
        })
      }
    },
    changeCallback (response) {
      let res = response.data
      this.scheduler_text = res.detail.current
      this.scheduler_flag = this.scheduler_text === 'PAUSED' ? 'error' : 'primary'
    },
    changeStatus (status) { // status为即将改变的状态
      if (status) { // 恢复
        instance.post('/back/cron/schedulers/resume').then(this.changeCallback)
      } else { // 暂停
        instance.post('/back/cron/schedulers/pause').then(this.changeCallback)
      }
    },
    toggleSchedulerFunc () {
      this.value1 = true
      this.toggleScheduler()
    },
    operateOptions (name) {
      if (name === 'edit') {
        this.toggleSchedulerFunc()
      }
    },
    toggleScheduler () {
      instance.get('/back/cron/schedulers').then((response) => {
        let res = response.data
        this.scheduler_text = res.detail.status
        this.formItem = {
          tz: res.detail.tz,
          type: res.detail.type,
          status: res.detail.status === 'PAUSED' ? Boolean(0) : Boolean(1)
        }
        if (this.scheduler_text === 'PAUSED') {
          this.scheduler_flag = 'error'
        } else {
          this.scheduler_flag = 'primary'
        }
      })
    },
    pauseJob (id) {
      instance.post('/back/cron/jobs/' + id + '/pause').then((response) => {
        let res = response.data
        if (res.ret === 0) {
          this.$Message.success(res.msg)
          instance.get('/back/cron/jobs').then(this.loadAllTasks)
        } else {
          this.$Message.error(res.msg)
        }
      })
    },
    recoverJob (id) {
      instance.post('/back/cron/jobs/' + id + '/resume').then((response) => {
        let res = response.data
        if (res.ret === 0) {
          this.$Message.success(res.msg)
          instance.get('/back/cron/jobs').then(this.loadAllTasks)
        } else {
          this.$Message.error(res.msg)
        }
      })
    },
    removeJob (id) {
      let that = this
      this.$Modal.confirm({
        title: '删除任务',
        content: '确认要删除该定时任务？',
        onOk: function () {
          instance.delete('/back/cron/jobs/' + id).then(function (response) {
            if (response.data.ret === 0) {
              that.$Message.success(response.data.msg)
              instance.get('/back/cron/jobs').then(that.loadAllTasks)
            } else {
              that.$Message.error(response.data.msg)
            }
          })
        }
      })
    },
    getSingleJob (id) {
      instance.get('/back/cron/jobs/' + id).then((response) => {
        let res = response.data
        if (res.ret === 0) {
          this.singleJob.name = res.detail.name
          this.singleJob.func = res.detail.func_ref
          this.singleJob = {
            name: res.detail.name,
            func: res.detail.func_ref,
            trigger: res.detail.trigger,
            next_run: new Date(Date(res.detail.next_run))
          }
          this.singleFlag = true
        } else {
          this.$Message.error('单个定时任务获取失败！')
        }
      })
    },
    cancelSingleModal () {
      this.singleFlag = false
    }
  },
  mounted () {
    instance.get('/back/cron/jobs').then(this.loadAllTasks)
    this.toggleScheduler()
  }
}
</script>

<style scoped>

</style>
