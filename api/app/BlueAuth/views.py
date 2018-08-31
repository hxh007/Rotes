# coding=utf-8

import re
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.models import User
from . import blue_auth
from .common import get_database


# 用户列表查询和用户创建
@blue_auth.route('/users', methods=['GET', 'POST'])
def users():
    result = {'code': 0, 'data': [], 'page': {}, 'msg': '用户信息查询成功'}
    if request.method == 'GET':
        # 数据库查询
        users = get_database(result=result, database=User, execute='all')
        if type(users) == dict:
            return jsonify(users)
        # 获取用户信息
        for user in users:
            result['data'].append(user.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        print(request.json)
        username = request.json.get('username')
        fullname = request.json.get('fullname')
        mobile = request.json.get('mobile')
        password = request.json.get('password')
        tag = request.json.get('tag')
        if not all([username, fullname, mobile, password, tag]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', mobile):
            result['code'] = 1
            result['msg'] = u'手机号不正确'
            return jsonify(result)
        try:
            user = User.query.filter_by(mobile=mobile).first()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return jsonify(result)
        if user:
            result['code'] = 1
            result['msg'] = u'用户已存在'
            return jsonify(result)
        user = User()
        user.username = username
        user.fullname = fullname
        user.mobile = mobile
        user.password = password
        user.tag = tag
        result = user.add(user)
        return jsonify(result)


# 用户信息查询，修改，删除
@blue_auth.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user(uid):
    result = {'code': 0, 'data': [], 'msg': '用户信息查询成功'}
    # 数据库查询
    user = get_database(result=result, database=User, execute='get', id=uid)
    if type(users) == dict:
        return jsonify(user)
    if request.method == 'GET':
        result['data'].append(user.to_dict())
        return jsonify(result)
    if request.method == 'PUT':
        username = request.json.get('username')
        fullname = request.json.get('fullname')
        mobile = request.json.get('mobile')
        password = request.json.get('password')
        tag = request.json.get('tag')
        is_department = request.json.get('is_department')
        status = request.json.get('status')
        remark = request.json.get('remark')
        if not all([username, fullname, mobile, password, tag]):
            result['code'] = 1
            result['msg'] = u'参数缺失'
            return jsonify(result)
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', mobile):
            result['code'] = 1
            result['msg'] = u'手机号不正确'
            return jsonify(result)
        if (is_department or status) not in [0, 1]:
            result['code'] = 1
            result['msg'] = u'参数错误'
            return jsonify(result)
        user.username = username
        user.fullname = fullname
        user.mobile = mobile
        user.password = password
        user.tag = tag
        user.is_department = is_department
        user.status = status
        user.remark = remark
        result = user.add(user)
        return jsonify(result)
    if request.method == 'DELETE':
        result = user.delete(user)
        return jsonify(result)


# 部门列表查询和部门创建
@blue_auth.route('/departments', methods=['GET', 'POST'])
def departments():
    pass


# 部门信息修改，修改，删改
@blue_auth.route('/departments/<int:did>', methods=['GET', 'PUT', 'DELETE'])
def department(did):
    pass
