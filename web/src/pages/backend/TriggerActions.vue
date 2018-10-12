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
              <Option v-for="(item, index) in userLists" :value="item.userId + '-' + item.phone + '-' + item.name" :key="index">{{ item.name }}</Option>
            </Select>
          </Col>
        </Row>
        <Row :style="{marginTop: '50px'}">
          <Col span="22" offset="1">
            <Card :style="{minHeight: '200px'}">
              <p slot="title">已选用户</p>
              <Tag v-if="selectedUsers.length > 0" type="dot" v-for="(item, index) in selectedUsers" :key="index" closable color="primary" @on-close="changeUsers">{{item}}</Tag>
              <span v-if="selectedUsers.length === 0">暂无已选用户</span>
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
                <Button type="primary">提交</Button>
                <Button style="margin-left: 8px">重置</Button>
              </FormItem>
            </Form>
          </TabPane>
          <TabPane label="发送短信">发送短信</TabPane>
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
      cityList: [
        {
          value: 'New York',
          label: 'New York'
        },
        {
          value: 'London',
          label: 'London'
        },
        {
          value: 'Sydney',
          label: 'Sydney'
        },
        {
          value: 'Ottawa',
          label: 'Ottawa'
        },
        {
          value: 'Paris',
          label: 'Paris'
        },
        {
          value: 'Canberra',
          label: 'Canberra'
        }
      ],
      userLists: [],
      defaultInfo: '',
      model10: [],
      selectedUsers: '',
      filterFlag: false
    }
  },
  methods: {
    changeUsers () {
      // 删除标签时的函数
    },
    changeUsersFunc (names) {
      console.log(names.length)
      for (let i = 0; i < names.length; i++) {
        let arr = names[i].split('-')
        this.selectedUsers.push(arr[2])
      }
    }
  },
  mounted () {
    this.userLists = []
    instance.get('/back/users').then((response) => {
      let res = response.data
      if (res.code === 0) {
        let len = res.data.length
        for (let i = 0; i < len; i++) {
          this.userLists.push({
            name: res.data[i].fullname,
            userId: res.data[i].id,
            phone: res.data[i].mobile
          })
        }
        this.filterFlag = true
      } else {
        this.$Message.error('用户列表加载失败！')
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
