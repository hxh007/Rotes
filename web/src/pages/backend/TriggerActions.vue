<template>
  <div style="margin: 20px">
    <div class="action-box" :style="{'overflow': 'hidden'}">
      <h3 :style="{'float': 'left'}">
        <div class="title" :style="{display: 'inline-block', marginRight: '10px', fontSize: '20px'}">
          触发操作
        </div>
        <router-link to="/backend/planTaskManage">
          <Icon type="ios-arrow-back" />返回
        </router-link>
      </h3>
    </div>
    <Divider/>
    <Row>
      <Col span="10">
        <Row>
          <Col span="6" :style="{fontSize: '14px', height: '30px', 'lineHeight': '30px', 'marginRight': '-10px'}">请选择用户:</Col>
          <Col span="18">
            <Select v-model="selectedUsers" multiple :filterable="filterFlag" @on-change="changeUsersFunc">
              <Option v-for="(item, index) in userLists" :value="item.userId + '-' + item.phone + '-' + item.name + '-' + item.ding_id" :key="index">{{ item.name }}</Option>
            </Select>
          </Col>
        </Row>
        <Row :style="{marginTop: '50px'}">
          <Col span="22" offset="1">
            <Card :style="{minHeight: '200px'}">
              <p slot="title">已选用户</p>
              <Tag v-if="userTags.length > 0" type="dot" v-for="(item, index) in userTags" :key="index" closable color="primary" @on-close="deleteUserTags(item.id)">{{item.name}}</Tag>
              <span v-if="userTags.length === 0">暂无已选用户</span>
            </Card>
          </Col>
        </Row>
      </Col>
      <Col span="10" offset="2">
        <Tabs type="card">
          <TabPane label="钉钉建群">
            <Form :style="{marginTop: '30px'}">
              <FormItem>
                <Input v-model="defaultInfo" type="textarea" :autosize="{minRows: 5,maxRows: 10}" placeholder="请输入初始化信息"></Input>
              </FormItem>
              <FormItem>
                <Button type="primary" @click="createGroups">提交</Button>
                <Button style="margin-left: 8px" @click="resetInfos">重置</Button>
              </FormItem>
            </Form>
          </TabPane>
          <TabPane label="发送短信">
            <Form :style="{marginTop: '30px'}">
              <FormItem>
                <Input v-model="messageInfo" type="textarea" :autosize="{minRows: 5,maxRows: 10}" placeholder="请输入初始化信息"></Input>
              </FormItem>
              <FormItem>
                <Button type="primary" @click="sendMessage">提交</Button>
                <Button style="margin-left: 8px" @click="resetMessage">重置</Button>
              </FormItem>
            </Form>
          </TabPane>
        </Tabs>
      </Col>
    </Row>
  </div>
</template>

<script>
import instance from '../../../libs/axios'
export default {
  name: 'triggerActions',
  data () {
    return {
      userLists: [],
      defaultInfo: '', // 默认内容
      messageInfo: '', // 短信内容
      userTags: [],
      selectedUsers: '',
      filterFlag: false
    }
  },
  methods: {
    deleteUserTags (id) {
      // 删除标签时的函数
      this.selectedUsers.forEach((item, index) => {
        let arr = item.split('-')
        if (id === arr[0]) {
          this.selectedUsers.splice(this.selectedUsers.indexOf(id), 1)
        }
      })
    },
    changeUsersFunc (names) {
      // 生成标签
      this.userTags = []
      this.selectedUsers.forEach((item, index) => {
        let arr = item.split('-')
        this.userTags.push({
          id: arr[0],
          phone: arr[1],
          name: arr[2]
        })
      })
    },
    createGroups () {
      if (this.defaultInfo.replace(/^(\s|\u00A0)+|(\s|\u00A0)+$/g, '') === '') {
        this.$Message.error('请输入初始化信息！')
      } else {
        let dingIds = []
        this.selectedUsers.forEach((item, index) => {
          let arr = item.split('-')
          if (arr[3] !== 'null') {
            dingIds.push(arr[3])
          }
        })
        if (dingIds.length > 0) {
          instance.post(process.env.API_ROOT + '/cron/ding', {
            userids: dingIds,
            message: this.defaultInfo
          }).then((response) => {
            let res = response.data
            if (res.ret === 0) {
              this.$Message.success(res.msg)
            } else {
              this.$Message.error(res.msg)
            }
          })
        } else {
          this.$Message.warning('所选用户无关联的钉_id，请前去关联！')
        }
      }
    },
    resetInfos () {
      this.defaultInfo = ''
    },
    sendMessage () {
      if (this.messageInfo.replace(/^(\s|\u00A0)+|(\s|\u00A0)+$/g, '') === '') {
        this.$Message.error('请输入短信内容！')
      } else {
        let phones = []
        let targetPhones = []
        this.selectedUsers.forEach((item, index) => {
          let arr = item.split('-')
          phones.push(arr[1])
        })
        // 去掉重复的电话号码
        phones.forEach((item, index) => {
          if (targetPhones.indexOf(item) === -1) {
            targetPhones.push(item)
          }
        })
        instance.post(process.env.API_ROOT + '/cron/sms', {
          mobiles: targetPhones,
          message: this.messageInfo
        }).then((response) => {
          let res = response.data
          if (res.ret === 0) {
            this.$Message.success(res.msg)
          } else {
            this.$Message.error(res.msg)
          }
        })
      }
    },
    resetMessage () {
      this.messageInfo = ''
    }
  },
  mounted () {
    this.userLists = []
    instance.get(process.env.API_ROOT + '/auth/users').then((response) => {
      let res = response.data
      if (res.code === 0) {
        let len = res.data.length
        for (let i = 0; i < len; i++) {
          this.userLists.push({
            name: res.data[i].fullname,
            userId: res.data[i].id,
            phone: res.data[i].mobile,
            ding_id: res.data[i].ding_id
          })
        }
        this.filterFlag = true
      } else {
        this.$Message.error('用户列表加载失败！')
      }
    })
    // 用短信模板渲染默认短信发送内容
    instance.get(process.env.API_ROOT + '/tempContent').then((response) => {
      let res = response.data
      if (res.code === 0) {
        this.messageInfo = res.data.tempContent
      }
    })
  }
}
</script>

<style scoped lang="stylus">
.return-box
  display inline-block
  cursor pointer
  font-size 18px
</style>
