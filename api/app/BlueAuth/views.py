# coding=utf-8

import re
from flask import jsonify, request
from sqlalchemy import or_

from app.models import User, Department, db_session_add, db_session_delete, Role, Management
from . import blue_auth
from .common import get_table, accept_para


# 用户列表查询和用户创建
@blue_auth.route('/users', methods=['GET', 'POST'])
def users():
    result = {'code': 0, 'data': [], 'msg': '用户列表查询成功'}
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
        user = get_table(result=result, table=User, terms=or_(User.username==paras[0], User.mobile==paras[2], User.tag==paras[4]), execute='first')
        if type(user) == dict:
            return jsonify(user)
        user = User()
        user.add_data(paras)
        result = db_session_add(user)
        result['msg'] = u'用户创建成功'
        return jsonify(result)


# 用户信息查询，修改，删除
@blue_auth.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user(uid):
    result = {'code': 0, 'data': [], 'msg': '用户信息查询成功'}
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
        result['msg'] = u'用户信息修改成功'
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(user)
        result['msg'] = u'用户删除成功'
        return jsonify(result)


# 部门列表查询和部门创建
@blue_auth.route('/departments', methods=['GET', 'POST'])
def departments():
    result = {'code': 0, 'data': [], 'msg': '部门列表查询成功'}
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
        result['msg'] = u'部门创建成功'
        return jsonify(result)


# 部门信息查询，修改，删改
@blue_auth.route('/departments/<int:did>', methods=['GET', 'PUT', 'DELETE'])
def department(did):
    result = {'code': 0, 'data': [], 'msg': '部门信息查询成功'}
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
        result['msg'] = u'部门信息修改成功'
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(department)
        result['msg'] = u'部门删除成功'
        return jsonify(result)


# 角色列表查询和角色创建
@blue_auth.route('/roles', methods=['GET', 'POST'])
def roles():
    result = {'code': 0, 'data': [], 'msg': '角色列表查询成功'}
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
        result['msg'] = u'角色创建成功'
        return jsonify(result)


# 角色信息查询、修改和删除
@blue_auth.route('/roles/<int:rid>', methods=['GET', 'PUT', 'DELETE'])
def role(rid):
    result = {'code': 0, 'data': [], 'msg': '角色信息查询成功'}
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
        result['msg'] = u'角色信息修改成功'
        return jsonify(result)
    if request.method == 'DELETE':
        result = db_session_delete(role)
        result['msg'] = u'角色删除成功'
        return jsonify(result)


# 管理员列表查询和创建
@blue_auth.route('/managements', methods=['GET', 'POST'])
def managements():
    result = {'code': 0, 'data': [], 'msg': '管理员列表查询成功'}
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
        result['msg'] = u'管理员创建成功'
        return jsonify(result)


# 管理员信息查询、修改和删除
@blue_auth.route('/managements/<int:mid>', methods=['GET', 'PUT', 'DELETE'])
def management(mid):
    pass


# 权限列表查询和创建
@blue_auth.route('/permissions', methods=['GET', 'POST'])
def permissions():
    pass


# 权限信息查询、修改和创建
@blue_auth.route('/permissions/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def permission(pid):
    pass
