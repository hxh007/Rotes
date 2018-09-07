# coding=utf-8

import re
from flask import jsonify, request
from sqlalchemy import or_, and_

from app.models import User, Department, db_session_add, db_session_delete, Role, Management, Permission, ActionType, \
    append_user, remove_user
from . import blue_auth
from .common import get_table, accept_para


# 资源
# 用户列表查询和用户创建
@blue_auth.route('/users', methods=['GET', 'POST'])
def users():
    result = {'code': 0, 'data': [], 'msg': u'用户列表查询成功'}
    if request.method == 'GET':
        # 数据库查询
        users = get_table(result=result, table=User, execute='all')
        if type(users) == dict:
            return jsonify(users)
        # 获取用户信息
        for user in users:
            result['data'].append(user.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        # username = request.json.get('username')
        # fullname = request.json.get('fullname')
        # mobile = request.json.get('mobile')
        # password = request.json.get('password')
        # tag = request.json.get('tag')

        # 获取参数
        para_list = ['username', 'fullname', 'mobile', 'password', 'tag']
        paras = accept_para(para_list)
        if not all([paras[0], paras[1], paras[2], paras[3]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', paras[2]):
            result['code'] = 1
            result['msg'] = u'手机号不正确'
            return jsonify(result)
        # try:
        #     user = User.query.filter(or_(User.username==paras[0], User.mobile==paras[2], User.tag==paras[4])).first()
        # except SQLAlchemyError:
        #     result['code'] = 1
        #     result['msg'] = u'数据查询失败'
        #     return jsonify(result)
        # if user:
        #     result['code'] = 1
        #     result['msg'] = u'用户已存在'
        #     return jsonify(result)

        # 查询用户是否存在
        user = get_table(result=result, table=User, terms=or_(User.username==paras[0], User.mobile==paras[2]), execute='first')
        if type(user) == dict:
            return jsonify(user)
        user = User()
        user.add_data(paras)
        result = db_session_add(user)
        return jsonify(result)


# 用户信息查询，修改，删除
@blue_auth.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user(uid):
    result = {'code': 0, 'data': [], 'msg': u'用户信息查询成功'}
    # 数据库查询
    user = get_table(result=result, table=User, execute='get', id=uid)
    if type(users) == dict:
        return jsonify(user)
    if request.method == 'GET':
        # to_dict() 返回用户信息字典
        result['data'].append(user.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        # username = request.json.get('username')
        # fullname = request.json.get('fullname')
        # mobile = request.json.get('mobile')
        # password = request.json.get('password')
        # tag = request.json.get('tag')
        # is_department = request.json.get('is_department')
        # status = request.json.get('status')
        # remark = request.json.get('remark')

        # 接收参数
        para_list = ['username', 'fullname', 'mobile', 'password', 'tag', 'is_department', 'status', 'remark']
        paras = accept_para(para_list)
        # 参数校验
        if not all([paras[0], paras[1], paras[2], paras[3]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', paras[2]):
            result['code'] = 1
            result['msg'] = u'手机号不正确'
            return jsonify(result)
        if (paras[5] or paras[6]) not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        # user.username = username
        # user.fullname = fullname
        # user.mobile = mobile
        # user.password = password
        # user.tag = tag
        # user.is_department = is_department
        # user.status = status
        # user.remark = remark

        # 修改用户信息
        user.change_data(paras)
        # 数据库提交
        result = db_session_add(user)
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(user)
        return jsonify(result)


# 部门列表查询和部门创建
@blue_auth.route('/departments', methods=['GET', 'POST'])
def departments():
    result = {'code': 0, 'data': [], 'msg': u'部门列表查询成功'}
    if request.method == 'GET':
        departments = get_table(result=result, table=Department, execute='all')
        if type(departments) == dict:
            return jsonify(departments)
        for department in departments:
            result['data'].append(department.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        para_list = ['name', 'alias']
        paras = accept_para(para_list)
        if not all(paras):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        department = get_table(result=result, table=Department, terms=or_(Department.name==paras[0], Department.alias==paras[1]), execute='first')
        if type(department) == dict:
            return jsonify(department)
        department = Department()
        department.add_data(paras)
        result = db_session_add(department)
        return jsonify(result)


# 部门信息查询，修改，删改
@blue_auth.route('/departments/<int:did>', methods=['GET', 'PUT', 'DELETE'])
def department(did):
    result = {'code': 0, 'data': [], 'msg': u'部门信息查询成功'}
    department = get_table(result=result, table=Department, execute='get', id=did)
    if type(department) == dict:
        return jsonify(department)
    if request.method == 'GET':
        result['data'].append(department.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        para_list = ['name', 'alias', 'status', 'remark']
        paras = accept_para(para_list)
        print(paras[0], paras[1], paras[2])
        if not all([paras[0], paras[1]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if paras[2] not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        department.change_data(paras)
        result = db_session_add(department)
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(department)
        return jsonify(result)


# 角色列表查询和角色创建
@blue_auth.route('/roles', methods=['GET', 'POST'])
def roles():
    result = {'code': 0, 'data': [], 'msg': u'角色列表查询成功'}
    if request.method == 'GET':
        roles = get_table(result=result, table=Role, execute='all')
        if type(roles) == dict:
            return jsonify(roles)
        for role in roles:
            result['data'].append(role.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        para_list = ['name', 'alias']
        paras = accept_para(para_list)
        if not paras[0]:
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        role = get_table(result=result, table=Role, execute='first', terms=Role.name==paras[0])
        if type(role) == dict:
            return jsonify(role)
        role = Role()
        role.add_data(paras)
        result = db_session_add(role)
        return jsonify(result)


# 角色信息查询、修改和删除
@blue_auth.route('/roles/<int:rid>', methods=['GET', 'PUT', 'DELETE'])
def role(rid):
    result = {'code': 0, 'data': [], 'msg': u'角色信息查询成功'}
    role = get_table(result=result, table=Role, execute='get', id=rid)
    if type(role) == dict:
        return jsonify(role)
    if request.method == 'GET':
        result['data'].append(role.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        para_list = ['name', 'alias', 'status', 'remark']
        paras = accept_para(para_list)
        if not paras[0]:
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if paras[2] not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        role.change_data(paras)
        result = db_session_add(role)
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(role)
        return jsonify(result)


# 管理员列表查询和创建
@blue_auth.route('/managements', methods=['GET', 'POST'])
def managements():
    result = {'code': 0, 'data': [], 'msg': u'管理员列表查询成功'}
    if request.method == 'GET':
        managements = get_table(result=result, table=Management, execute='all')
        if type(managements) == dict:
            return jsonify(managements)
        for management in managements:
            result['data'].append(management.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        para_list = ['name', 'alias']
        paras = accept_para(para_list)
        if not paras[0]:
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        management = get_table(result=result, table=Management, execute='first', terms=Management.name==paras[0])
        if type(management) == dict:
            return jsonify(management)
        management = Management()
        management.add_data(paras)
        result = db_session_add(management)
        return jsonify(result)


# 管理员信息查询、修改和删除
@blue_auth.route('/managements/<int:mid>', methods=['GET', 'PUT', 'DELETE'])
def management(mid):
    result = {'code': 0, 'data': [], 'msg': u'管理员信息查询成功'}
    management = get_table(result=result, table=Management, execute='get', id=mid)
    if type(management) == dict:
        return jsonify(management)
    if request.method == 'GET':
        result['data'].append(management.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        para_list = ['name', 'alias', 'status', 'remark']
        paras = accept_para(para_list)
        if not paras[0]:
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if paras[2] not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        management.change_data(paras)
        result = db_session_add(management)
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(management)
        return jsonify(result)


# 权限列表查询和创建
@blue_auth.route('/permissions', methods=['GET', 'POST'])
def permissions():
    result = {'code': 0, 'data': [], 'msg': u'权限列表查询成功'}
    if request.method == 'GET':
        permissions = get_table(result=result, table=Permission, execute='all')
        if type(permissions) == dict:
            return jsonify(permissions)
        for permission in permissions:
            result['data'].append(permission.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        para_list = ['alias', 'codename', 'department_id']
        paras = accept_para(para_list)
        if not all([paras[0], paras[1]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        actions = get_table(result=result, table=ActionType, execute='with_entities', terms=ActionType.codename)
        if type(actions) == dict:
            return jsonify(actions)
        if (paras[1],) not in actions:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        permission = get_table(result=result, table=Permission, execute='first', terms=and_(Permission.alias==paras[0], Permission.codename==paras[1]))
        if type(permission) == dict:
            return jsonify(permission)
        permission = Permission()
        permission.add_data(paras)
        result = db_session_add(permission)
        return jsonify(result)


# 权限信息查询、修改和删除
@blue_auth.route('/permissions/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def permission(pid):
    result = {'code': 0, 'data':[], 'msg': u'权限信息查询成功'}
    permission = get_table(result=result, table=Permission, execute='get', id=pid)
    if type(permission) == dict:
        return jsonify(permission)
    if request.method == "GET":
        result['data'].append(permission.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        para_list = ['alias', 'codename', 'status', 'remark']
        paras = accept_para(para_list)
        if not all([paras[0], paras[1]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if paras[2] not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        permission.change_data(paras)
        result = db_session_add(permission)
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(permission)
        return jsonify(result)


# 操作类型查询，添加
@blue_auth.route('/actiontypes')
def action_type():
    result = {'code': 0, 'data': [], 'msg': u'查询成功'}
    if request.method == "GET":
        actions = get_table(result=result, table=ActionType, execute='all')
        if type(actions) == dict:
            return jsonify(actions)
        for action in actions:
            result['data'].append(action.to_dict())
        return jsonify(result)
    if request.method == "POST":
        para_list = ['codename', 'alias']
        paras = accept_para(para_list)
        if not all([paras[0], paras[1]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        action = get_table(result=result, table=ActionType, execute='first',
                               terms=ActionType.codename == paras[0])
        if type(action) == dict:
            return jsonify(action)
        action = ActionType()
        action.add_data(paras)
        result = db_session_add(action)
        return jsonify(result)


# 关系
# 部门用户查询，添加， 删除
@blue_auth.route('/departments/users/<int:did>', methods = ['GET', 'POST', 'DELETE'])
def department_user(did):
    result = {'code': 0, 'data': [], 'msg': u'部门用户信息查询成功'}
    # 部门和部门用户查询
    department = get_table(result=result, table=Department, execute='get', id=did)
    if type(department) == dict:
        return jsonify(department)
    d_users = get_table(result=result, execute='relationship', relationship=department.users)
    if type(d_users) == dict:
        return jsonify(d_users)
    # 返回部门用户信息
    if request.method == 'GET':
        # 部门无用户
        for d_user in d_users:
            result['data'].append(d_user.to_dict())
        return jsonify(result)
    # 获取用户id
    uid = request.json.get('uid')
    # 参数校验
    if not uid:
        result['code'] = 1
        result['msg'] = u'参数缺失'
        return jsonify(result)
    try:
        uid = int(uid)
    except Exception:
        result['code'] = 1
        result['msg'] = u'数据格式错误'
        return jsonify(result)
    # 需要添加或删除的用户
    user = get_table(result=result, table=User, execute='get', id=uid)
    if type(user) == dict:
        return jsonify(user)
    # 部门用户信息添加
    if request.method == 'POST':
        # 用户是否属于该部门
        if user in d_users:
            result['code'] = 1
            result['msg'] = u'该用户已添加'
            return jsonify(result)
        # 添加用户
        result = append_user(department, user)
        return jsonify(result)
    # 删除部门用户
    if request.method == 'DELETE':
        # 用户是否属于该部门
        if user not in d_users:
            result['code'] = 1
            result['msg'] = u'用户不存在，删除失败'
            return jsonify(result)
        # 删除用户
        result = remove_user(department, user)
        return jsonify(result)


# 部门角色查询、添加和删除
@blue_auth.route('/departments/roles/<int:did>', methods=['GET', 'POST', 'DELETE'])
def department_roles(did):
    result = {'code': 0, 'data': [], 'msg': u'部门角色信息查询成功'}
    # 部门和部门角色查询
    department = get_table(result=result, table=Department, execute='get', id=did)
    if type(department) == dict:
        return jsonify(department)
    d_roles = get_table(result=result, execute='relationship', relationship=department.roles)
    if type(d_roles) == dict:
        return jsonify(d_roles)
    # 返回部门角色信息
    if request.method == 'GET':
        # 部门无角色
        for d_role in d_roles:
            result['data'].append(d_role.to_dict())
        return jsonify(result)
    # 获取角色id
    rid = request.json.get('rid')
    # 参数校验
    if not rid:
        result['code'] = 1
        result['msg'] = u'参数缺失'
        return jsonify(result)
    try:
        rid = int(rid)
    except Exception:
        result['code'] = 1
        result['msg'] = u'数据格式错误'
        return jsonify(result)
    # 需要添加或删除的角色
    role = get_table(result=result, table=Role, execute='get', id=rid)
    if type(role) == dict:
        return jsonify(role)
    # 部门角色信息添加
    if request.method == 'POST':
        # 角色是否已添加
        if role in d_roles:
            result['code'] = 1
            result['msg'] = u'该角色已添加'
            return jsonify(result)
        # 添加角色
        result = department.append_role(role)
        return jsonify(result)
    # 删除部门角色
    if request.method == 'DELETE':
        # 角色是否属于该部门
        if role not in d_roles:
            result['code'] = 1
            result['msg'] = u'角色不存在，删除失败'
            return jsonify(result)
        # 删除角色
        result = department.remove_role(role)
        return jsonify(result)


# 角色用户查询、添加和删除
@blue_auth.route('/roles/users/<int:rid>', methods=['GET', 'POST', 'DELETE'])
def role_users(rid):
    result = {'code': 0, 'data': [], 'msg': u'角色用户信息查询成功'}
    # 角色和角色用户查询
    role = get_table(result=result, table=Role, execute='get', id=rid)
    if type(role) == dict:
        return jsonify(role)
    r_users = get_table(result=result, execute='relationship', relationship=role.users)
    if type(r_users) == dict:
        return jsonify(r_users)
    # 返回角色用户信息
    if request.method == 'GET':
        # 角色无用户
        for r_user in r_users:
            result['data'].append(r_user.to_dict())
        return jsonify(result)
    # 获取用户id
    uid = request.json.get('uid')
    # 参数校验
    if not uid:
        result['code'] = 1
        result['msg'] = u'参数缺失'
        return jsonify(result)
    try:
        uid = int(uid)
    except Exception:
        result['code'] = 1
        result['msg'] = u'数据格式错误'
        return jsonify(result)
    # 需要添加或删除的用户
    user = get_table(result=result, table=User, execute='get', id=uid)
    if type(user) == dict:
        return jsonify(user)
    # 角色用户信息添加
    if request.method == 'POST':
        # 用户是否属于该角色
        if user in r_users:
            result['code'] = 1
            result['msg'] = u'该用户已添加'
            return jsonify(result)
        # 添加用户
        result = append_user(role, user)
        return jsonify(result)
    # 删除角色用户
    if request.method == 'DELETE':
        # 用户是否属于该角色
        if user not in r_users:
            result['code'] = 1
            result['msg'] = u'用户不存在，删除失败'
            return jsonify(result)
        # 删除
        result = remove_user(role, user)
        return jsonify(result)


# 管理员用户查询、添加和删除
@blue_auth.route('/managements/users/<int:mid>', methods=['GET', 'POST', 'DELETE'])
def management_users(mid):
    result = {'code': 0, 'data': [], 'msg': u'管理人员信息查询成功'}
    # 管理和管理人员查询
    management = get_table(result=result, table=Management, execute='get', id=mid)
    if type(management) == dict:
        return jsonify(management)
    m_users = get_table(result=result, execute='relationship', relationship=management.users)
    if type(m_users) == dict:
        return jsonify(m_users)
    # 返回管理用户信息
    if request.method == 'GET':
        # 角色无用户
        for m_user in m_users:
            result['data'].append(m_user.to_dict())
        return jsonify(result)
    # 获取用户id
    uid = request.json.get('uid')
    # 参数校验
    if not uid:
        result['code'] = 1
        result['msg'] = u'参数缺失'
        return jsonify(result)
    try:
        uid = int(uid)
    except Exception:
        result['code'] = 1
        result['msg'] = u'数据格式错误'
        return jsonify(result)
    # 需要添加或删除的用户
    user = get_table(result=result, table=User, execute='get', id=uid)
    if type(user) == dict:
        return jsonify(user)
    # 管理员信息添加
    if request.method == 'POST':
        # 用户是否属于管理员
        if user in m_users:
            result['code'] = 1
            result['msg'] = u'该用户已添加'
            return jsonify(result)
        # 添加
        result = append_user(management, user)
        return jsonify(result)
    # 删除管理用户
    if request.method == 'DELETE':
        # 用户是否是管理员
        if user not in m_users:
            result['code'] = 1
            result['msg'] = u'用户不存在，删除失败'
            return jsonify(result)
        # 删除
        result = remove_user(management, user)
        return jsonify(result)


# 管理员权限查询、添加和删除
@blue_auth.route('/managements/permissions/<int:mid>', methods=['GET', 'POST', 'DELETE'])
def management_permissions(mid):
    result = {'code': 0, 'data': [], 'msg': u'管理员权限信息查询成功'}
    # 管理和管理权限查询
    management = get_table(result=result, table=Management, execute='get', id=mid)
    if type(management) == dict:
        return jsonify(management)
    m_permissions = get_table(result=result, execute='relationship', relationship=management.permissions)
    if type(m_permissions) == dict:
        return jsonify(m_permissions)
    # 返回管理权限信息
    if request.method == 'GET':
        # 无权限
        for m_permission in m_permissions:
            result['data'].append(m_permission.to_dict())
        return jsonify(result)
    # 获取权限id
    pid = request.json.get('pid')
    # 参数校验
    if not pid:
        result['code'] = 1
        result['msg'] = u'参数缺失'
        return jsonify(result)
    try:
        pid = int(pid)
    except Exception:
        result['code'] = 1
        result['msg'] = u'数据格式错误'
        return jsonify(result)
    # 需要添加或删除的权限
    permission = get_table(result=result, table=Permission, execute='get', id=pid)
    if type(permission) == dict:
        return jsonify(permission)
    # 管理权限信息修改
    if request.method == 'POST':
        # 权限是否属于该管理
        if permission in m_permissions:
            result['code'] = 1
            result['msg'] = u'该权限已添加'
            return jsonify(result)
        # 添加权限
        result = management.append_permission(permission)
        return jsonify(result)
    # 删除权限
    if request.method == 'DELETE':
        # 权限是否属于该管理员
        if permission not in m_permissions:
            result['code'] = 1
            result['msg'] = u'权限不存在，删除失败'
            return jsonify(result)
        # 删除
        result = management.remove_permission(permission)
        return jsonify(result)
