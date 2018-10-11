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
    </div>
    <Divider/>
    <Table border :columns="columns" :data="taskLists"></Table>
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
          key: 'next_run'
        },
        {
          title: '操作',
          key: '操作',
          width: 300,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'warning',
                  size: 'small'
                },
                on: {
                  click: () => {
                    // 暂停
                  }
                }
              }, '暂停'),
              h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                on: {
                  click: () => {
                    // 暂停
                  }
                }
              }, '恢复'),
              h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                on: {
                  click: () => {
                    // 暂停
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
                    this.remove(params.row.id)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      taskLists: [],
      disabled: true
    }
  },
  methods: {
    loadAllTasks (response) {
      let res = response.data
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
