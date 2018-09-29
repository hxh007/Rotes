# coding=utf-8

import re
from flask import jsonify, request, g
from sqlalchemy import or_, and_

from app.BlueAuth.auth import Authentication
from app.models import (User, Department, Role, Management, Permission,
                        ActionType, db_session_add, db_session_delete,
                        query_relation, append_relation, remove_relation)
from . import blue_auth
from .common import (get_table, accept_para, response_return, TableTelationType)


# 权限管理 超级管理才能访问
@blue_auth.before_request
def auth_supper():
    # 判断登录用户
    response_data = Authentication.jwt_token_verify()
    if response_data['code']:
        return jsonify(response_data)
    # 用户所在管理组
    managerList = g.managerList
    if ('S_MANAGEMENT' not in managerList) and request.method != 'GET':
        return jsonify(response_return(3, u'没有权限访问'))


# 资源
# 用户列表查询和用户创建
@blue_auth.route('/users', methods=['GET', 'POST'])
def users():
    result = {'code': 0, 'data': [], 'msg': u'用户列表查询成功'}
    if request.method == 'GET':
        # 页数，默认1
        page = request.args.get('page', 1, type=int)
        # 一页的数据，默认15
        per_page = request.args.get('per_page', 15, type=int)
        # 数据库查询
        paginate = get_table(result=result, table=User, execute='paginate', terms=(User.ctime.desc()), page=page, per_page=per_page)
        if type(paginate) == dict:
            return jsonify(paginate)
        users = paginate.items
        total_page = paginate.pages
        current_page = paginate.page
        # 获取用户信息
        for user in users:
            result['data'].append(user.to_dict())
        result['total_page'] = total_page
        result['current_page'] = current_page
        return jsonify(result)
    if request.method == 'POST':
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
    if type(user) == dict:
        return jsonify(user)
    if request.method == 'GET':
        # to_dict() 返回用户信息字典
        result['data'].append(user.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        # 接收参数
        para_list = ['username', 'fullname', 'mobile', 'password', 'tag', 'is_department', 'status', 'remark', 'is_default_ops']
        paras = accept_para(para_list)
        # 参数校验
        if not all([paras[0], paras[1], paras[2]]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', paras[2]):
            result['code'] = 1
            result['msg'] = u'手机号不正确'
            return jsonify(result)
        if (paras[5] or paras[6] or paras[8]) not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        # 密码存在  修改密码
        if paras[3]:
            # 修改用户信息
            user.change_data(paras)
            user.password = paras[3]
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
        if (paras[2]) not in [0, 1]:
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


# 管理组列表查询和创建
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


# 管理组信息查询、修改和删除
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
        if management.name == 'S_MANAGEMENT':
            result['code'] = 1
            result['msg'] = u'不允许删除超级管理'
            return jsonify(result)
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
        try:
            management = Management.query.filter_by(name='S_MANAGEMENT').first()
        except Exception:
            return jsonify(response_return(1, u'数据查询出错'))
        if not management:
            return jsonify(response_return(1, '数据不存在'))
        permission.p_managements.append(management)
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
        para_list = ['alias', 'codename', 'status', 'remark', 'department_id']
        paras = accept_para(para_list)
        if not all([paras[0], paras[1], paras[4]]):
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
@blue_auth.route('/actiontypes', methods=['GET', 'POST'])
def action_types():
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


# 操作类型删除
@blue_auth.route('/actiontypes/<int:aid>', methods = ['DELETE'])
def action_type(aid):
    result = {'code': 0, 'data': [], 'msg': u'查询成功'}
    action = get_table(result=result, table=ActionType, execute='get', id=aid)
    if type(action) == dict:
        return jsonify(action)
    result = db_session_delete(action)
    return jsonify(result)


# 关系查询、添加、删除
@blue_auth.route('/relations', methods=['GET', 'POST', 'DELETE'])
def many_to_many():
    # 父级资源id
    fid = request.args.get('fid', None, type=int)
    # 关系类型
    genre = request.args.get('genre', None, type=int)
    if not all([fid, genre]):
        return jsonify(response_return(1, u'参数缺失'))
    genre_dict = TableTelationType.genre.get(genre, None)
    if not genre_dict:
        return jsonify(response_return(1, u'genre无效'))
    # 查询
    f_table = get_table(result=response_return(), table=genre_dict['f_table'], execute='get', id=fid)
    if isinstance(f_table, dict):
        return jsonify(response_return(1, u'数据查询失败或无此数据'))
    # 子资源
    f_s_table = get_table(result=response_return(), execute='relationship', relationship=query_relation(f_table, genre))
    if isinstance(f_s_table, dict):
        return jsonify(response_return(1, u'数据查询失败'))
    # 返回关系信息
    if request.method == 'GET':
        # 查询类型
        not_add = request.args.get('not_add', None, type=int)
        data = []
        if not not_add:
            for s in f_s_table:
                data.append(s.to_dict())
        # 未添加子资源
        else:
            s_table = genre_dict['s_table'].query.all()
            for s in s_table:
                if s not in f_s_table:
                    data.append(s.to_dict())
        return jsonify(response_return(0, u'关系查询成功', data=data))
    # 子级资源id
    sid = request.json.get('sid')
    # 子表id校验
    if not sid:
        return jsonify(response_return(1, u'sid参数缺失'))
    try:
        sid = int(sid)
    except Exception:
        return jsonify(response_return(1, u'sid格式错误'))
    # 需要添加或删除的关系
    s_table= get_table(result=response_return(), table=genre_dict['s_table'], execute='get', id=sid)
    if isinstance(s_table, dict):
        return jsonify(response_return(1, u'数据查询失败或无数据'))
    # 添加关系
    if request.method == 'POST':
        if s_table in f_s_table:
            return jsonify(response_return(1, u'关系已存在'))
        # 添加关系
        result = append_relation(f_table, s_table, genre)
        return jsonify(result)
    # 删除关系
    if request.method == 'DELETE':
        if s_table not in f_s_table:
            return jsonify(response_return(1, u'关系不存在，删除失败'))
        result = remove_relation(f_table, s_table, genre)
        return jsonify(result)
