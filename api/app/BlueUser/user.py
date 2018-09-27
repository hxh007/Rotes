# coding=utf-8
import re

import datetime

from collections import defaultdict
from flask import jsonify, g

from app import Redis
from app.BlueUser.common import ClientType
from app.models import User, db_session_add, Department
from app.BlueUser import blue_user
from app.BlueAuth.common import accept_para, response_return, get_table
from app.BlueAuth.auth import Authentication


# 注册
@blue_user.route('/register', methods=['POST'])
def auth_register():
    para_list = ['username', 'fullname', 'mobile', 'password', 'client_type']
    paras = accept_para(para_list)
    # 登录类型
    try:
        client_type = int(paras[4])
    except Exception:
        return jsonify(response_return(1, u'client_type格式错误'))
    promise = {
        ClientType.USER_NAME: __client_register_by_username,
        ClientType.USER_DING: __client_register_by_ding
    }
    return jsonify(promise[client_type](paras))

# 用户名注册
def __client_register_by_username(paras):
    # 参数完整性
    if not all([paras[0], paras[1]]):
        return response_return(1, u'用户名和姓名不能为空')
    # 手机号格式
    if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', paras[2]):
        return response_return(1, u'手机号不正确')
    # 密码长度
    if not re.match(r'^[a-zA-Z]\w{6,20}$', paras[3]):
        return response_return(1, u'密码以字母开头，长度在6~20之间，只能包含字母、数字')
    # 查询用户名是否已注册
    user_name = get_table(result=response_return(), table=User,
                          terms=(User.username==paras[0]), execute='first'
                          )
    if isinstance(user_name, dict):
        return response_return(1, u'该用户名已注册或数据库查询失败')
    # 查询手机号是否已注册
    user_mobile = get_table(result=response_return(), table=User,
                            terms=(User.mobile==paras[2]), execute='first'
                            )
    if isinstance(user_mobile, dict):
        return response_return(1, u'该手机号已注册或数据库查询失败')
    # 写入数据库
    user = User()
    user.username = paras[0]
    user.fullname = paras[1]
    user.mobile = paras[2]
    user.password = paras[3]
    result = db_session_add(user)
    return result

# 钉钉绑定
def __client_register_by_ding(paras):
    pass


# 用户登录
@blue_user.route('/login', methods=['POST'])
def auth_login():
    para_list = ['username', 'password', 'client_type', 'ding_id']
    paras = accept_para(para_list)
    # 登录类型
    try:
        client_type = int(paras[2])
    except Exception:
        return jsonify(response_return(1, u'client_type格式错误'))
    promise = {
        ClientType.USER_NAME: __client_login_by_username,
        ClientType.USER_DING: __client_login_by_ding
    }
    return jsonify(promise[client_type](paras))


# 用户名登录
def __client_login_by_username(paras):
    if not all([paras[0], paras[1]]):
        return response_return(1, u'用户名或密码不能为空')
    try:
        user = User.query.filter_by(username=paras[0]).first()
    except Exception:
        return response_return(1, u'数据查询失败')
    if not user:
        return response_return(1, u'该用户不存在')
    if not user.status:
        return response_return(1, u'该用户已被禁用')
    # 检查用户名和密码
    if not (user.check_password(password=paras[1])):
        return response_return(1, u'用户名或密码错误')
    # 获取用户管理身份
    group_list = [g.name for g in __user_manager_list(user)]
    if isinstance(group_list, dict):
        return group_list
    # 获取用户部门
    depart_list = __user_depart_list(user)
    if isinstance(group_list, dict):
        return depart_list
    user.login_time = datetime.datetime.now()
    res = db_session_add(user)
    if res['code'] == 1:
        return jsonify(res)
    # 生成jwt_token
    jwt_token = Authentication.encode_jwt_token(user)
    if isinstance(jwt_token, dict):
        return jsonify(jwt_token)
    # 将jwt_token写入redis
    Authentication.set_redis_jwt(user.mobile, jwt_token)
    data = {
        'user': user.to_dict(),
        'jwt_token': jwt_token,
        'group_list': group_list,
        'depart_list': depart_list
    }
    return response_return(0, u'登录成功', data=data)


# 钉钉登录
def __client_login_by_ding(paras):
    pass


# 退出登录
@blue_user.route('/logout')
def auth_logout():
    '''
    退出登录：删除redis中的jwt
    :return:
    '''
    Authentication.jwt_token_verify()
    uid = g.user_id
    Authentication.del_redis_jwt(uid)
    return jsonify(response_return(0, u'退出成功'))

# 获取用户的管理身份列表
def __user_manager_list(user):
    try:
        manager_list = user.u_managements.all()
    except Exception:
        return response_return(1, u'数据查询失败')
    return manager_list

# 获取用户所在部门列表
def __user_depart_list(user):
    try:
        departments = user.departments.all()
    except Exception:
        return response_return(1, u'数据查询失败')
    depart_list = []
    for department in departments:
        depart_list.append(department.to_dict())
    return depart_list

# 获取用户所有权限
def __user_permission_list(user):
    manager_list = __user_manager_list(user)
    permission_list = defaultdict(dict)
    for manager in manager_list:
        for permission in manager.permissions.all():
            try:
                department = Department.query.get(int(permission.department_id))
            except Exception:
                return dict()
            if not permission_list.get(department.id):
                permission_list[department.id]['departName'] = department.name
                permission_list[department.id]['departAlias'] = department.alias
                permission_list[department.id]['pLists'] = list()
            permission_list[department.id]['pLists'].append(permission.codename)
    return permission_list


# 登录用户信息查询
@blue_user.route('/login_user_info')
def user_info():
    # 登录验证
    response_data = Authentication.jwt_token_verify()
    if response_data['code']:
        return jsonify(response_data)
    user_id = g.user_id
    user = get_table(result=response_return(), table=User, execute='get', id=user_id)
    if isinstance(user, dict):
        return jsonify(user)
    data = {
        'user_info': user.to_dict(),
        'permission_list': __user_permission_list(user),
        'depart_list': __user_depart_list(user),
        'group_list':[m.to_dict() for m in __user_manager_list(user)]
    }
    return jsonify(response_return(0, u'信息查询成功', data=data))
