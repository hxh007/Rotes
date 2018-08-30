# coding=utf-8

from datetime import datetime

from flask import render_template, request, jsonify

from . import blue_watch
from app import db
from app.models import OnDuty, TempText


# 值班列表及新增(部门负责人具有的操作）
@blue_watch.route('/onduty', methods=['GET', 'POST'])
def ondutyList():
    result = {'code': 0, 'msg': u'查询值班信息成功'}
    if request.method == 'GET':
        # 返回值班列表信息
        if request.is_json:
            data = request.get_json()
            department_name = data.get('department_name')

            pass
        else:
            result['code'] = 1
            result['msg'] = u'接收不到参数'
            return jsonify(result)
    if request.method == 'POST':
        # 新增值班记录
        if request.is_json:
            # 接收参数
            data = request.get_json()
            department_name = data.get('department_name')
            principal = data.get('principal')
            role_name = data.get('role_name')
            name = data.get('name')
            duty_time = data.get('duty_time')
            # 参数校验
            if not all([department_name, principal, role_name, role_name, name, duty_time]):
                result['code'] = 1
                result['msg'] = u'参数不完整'
                return jsonify(result)
            # 逻辑处理，入库
            onduty_add = OnDuty(department_name=department_name, principal=principal, role_name=role_name, name=name, duty_time=duty_time)
            db.session.add(onduty_add)
            db.session.commit()
            db.session.close()
            result['msg'] = u'添加值班记录成功'
            return jsonify(result)
        else:
            result['code'] = 1
            result['msg'] = u'接收不到参数'
            return jsonify(result)

        pass
    return 'OK'


# 单个值班记录编辑(部门负责人具有的操作）
@blue_watch.route('/onduty/<int:onduty_id>', methods=['GET', 'PUT', 'DELETE'])
def onduty(onduty_id):
    result = {'code': 0, 'data': {}, 'msg': u'查询值班记录成功'}
    onduty_change = OnDuty.query.filter_by(id=onduty_id).first()
    if not onduty_change:
        result['code'] = 1
        result['msg'] = u'无此值班记录'
        return jsonify(result)
    if request.method == 'GET':
        result['data']['onduty_id'] = onduty_id
        result['data']['department_name'] = onduty_change.department_name
        result['data']['principal'] = onduty_change.principal
        result['data']['role_name'] = onduty_change.role_name
        result['data']['name'] = onduty_change.name
        result['data']['duty_time'] = onduty_change.duty_time
        return jsonify(result)
    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            department_name = data.get('department_name')
            principal = data.get('principal')
            role_name = data.get('role_name')
            name = data.get('name')
            duty_time = data.get('duty_time')
            if not all([department_name, principal, role_name, name, duty_time]):
                result['code'] = 1
                result['msg'] = u'参数不完整'
                return jsonify(result)
            onduty_change.department_name = department_name
            onduty_change.principal = principal
            onduty_change.role_name = role_name
            onduty_change.name = name
            onduty_change.duty_time = duty_time
            db.session.commit()
            result['msg'] = u'修改值班记录成功'
            return jsonify(result)
        else:
            result['code'] = 1
            result['msg'] = u'接收不到参数'
            return jsonify(result)
    elif request.method == 'DELETE':
        db.session.delete(onduty_change)
        db.session.commit()
        db.session.close()
        result['msg'] = u'已删除此条值班记录'
        return jsonify(result)
