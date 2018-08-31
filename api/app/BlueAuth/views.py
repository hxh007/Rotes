# coding=utf-8

import re
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.models import User
from . import blue_auth


# 用户列表查询和用户创建
@blue_auth.route('/users', methods=['GET', 'POST'])
def users():
    result = {'code': 0, 'data': [], 'page':{}, 'msg': '用户信息查询成功'}
    if request.method == 'GET':
        try:
            users = User.query.all()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'用户数据查询失败'
            return jsonify(result)
        if not users:
            result['code'] = 1
            result['msg'] = u'无用户信息'
            return jsonify(result)
        for user in users:
            result['data'].append(user.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        username = request.json.get('username')
        fullname = request.json.get('fullname')
        mobile = request.json.get('mobile')
        tag = request.json.get('tag')
        is_department = request.json.get('is_department')
        if not all([username, fullname, mobile, tag]):
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
        user.tag = tag
        user.is_department = is_department
        result=user.add(user)
        return jsonify(result)
