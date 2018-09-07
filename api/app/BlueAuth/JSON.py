# coding=utf-8
"""
资源curd
1 用户列表查询
    1 接收
    2 返回
    {
        {
            "id": "用户id",
            "username": "用户名",
            "fullname": "姓名",
            "mobile": "手机号",
            "password": "密码",
            "tag": "工号",
            "is_department": "部门负责人",
            "ding_id": "钉钉id",
            "status": "状态",
            "remark": "备注",
            "login_time": "登录时间",
            "last_change": "修改时间"
        },
    {
2 用户创建
    1 接收
    {
        "username": "用户名",
        "fullname": "姓名",
        "mobile": "手机号",
        "password": "密码",
        "tag": "工号"
    }
    2 返回
    {
        "code": 0,
        "msg": "数据库提交成功"
    }
3 用户信息查询 /auth/users/uid  GET
    1 接收
    2 返回
    {
        "id": "用户id",
        "username": "用户名",
        "fullname": "姓名",
        "mobile": "手机号",
        "password": "密码",
        "tag": "工号",
        "is_department": "部门负责人",
        "ding_id": "钉钉id",
        "status": "状态",
        "remark": "备注",
        "login_time": "登录时间",
        "last_change": "修改时间"
    }
4 用户信息修改 /auth/users/uid  PUT
    1 接收
    {
        "username": "用户名",
        "fullname": "姓名",
        "mobile": "手机号",
        "password": "密码",
        "tag": "工号",
        "is_department": "部门负责人",
        "status": "状态",
        "remark": "备注"
    }
    2 返回
    {
        "code": 0,
        "msg": "数据库提交成功"
    }
5 用户信息删除 /auth/users/uid  DELETE
    1 接收
    2 返回
    {
        "code": 0,
        "msg": "数据库提交成功"
    }
6 部门列表查询
    1 接收
    2 返回
    {
        "id": "用户id",
        "name": "部门En",
        "alias": "部门Zh",
        "remark": "备注",
        "status": "状态",
        "last_change": "修改时间"
    }
7 部门创建
    1 接收
    2 返回











关系
1 部门和用户
/auth/departments/users
    1 接收
    2 返回

"""
