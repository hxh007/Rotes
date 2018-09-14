<template>
  <div>
    排班记录
    <div class="search-box">
      <Form :model="formItem" :label-width="80">
        <Row>
          <Col span="8">
            <FormItem label="部门">
              <Select v-model="formItem.select">
                <Option value="SYS">系统运维部</Option>
                <Option value="NET">网络安全部</Option>
                <Option value="TECH">技术运营部</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="8">
            <FormItem label="排班角色">
              <Select v-model="formItem.select">
                <Option value="beijing">一线</Option>
                <Option value="shanghai">二线</Option>
                <Option value="shenzhen">2.5线</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="8">

          </Col>
        </Row>
      </Form>
    </div>
    <div class="show-box">
      <Table border :columns="columns7" :data="data6"></Table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Schedule',
  data () {
    return {
      formItem: {
        select: ''
      },
      columns7: [
        {
          title: 'Name',
          key: 'name',
          render: (h, params) => {
            return h('div', [
              h('Icon', {
                props: {
                  type: 'person'
                }
              }),
              h('strong', params.row.name)
            ])
          }
        },
        {
          title: 'Age',
          key: 'age'
        },
        {
          title: 'Address',
          key: 'address'
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
              }, 'View'),
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
              }, 'Delete')
            ])
          }
        }
      ],
      data6: [
        {
          name: 'John Brown',
          age: 18,
          address: 'New York No. 1 Lake Park'
        },
        {
          name: 'Jim Green',
          age: 24,
          address: 'London No. 1 Lake Park'
        },
        {
          name: 'Joe Black',
          age: 30,
          address: 'Sydney No. 1 Lake Park'
        },
        {
          name: 'Jon Snow',
          age: 26,
          address: 'Ottawa No. 2 Lake Park'
        }
      ]
    }
  },
  mounted () {
    // console.log(this.$route.query.dateRange)
  }
}
</script>

<style scoped lang="stylus">
.search-box
  margin-top 20px
</style>
