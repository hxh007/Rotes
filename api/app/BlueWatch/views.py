# coding=utf-8

from datetime import datetime

from flask import render_template, request, jsonify

from . import blue_watch
from app import db
from app.models import Duty, TempText


# 值班列表及新增(部门负责人具有的操作）
@blue_watch.route('/duty', methods=['GET', 'POST'])
def dutyList():
    result = {'code': 0, 'msg': u'查询值班信息成功'}
    if request.method == 'GET':
        # 返回值班列表信息
        if request.is_json:
            data = request.get_json()
            depart = data.get('depart')

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
            depart = data.get('depart')
            role = data.get('role')
            duty_name = data.get('duty_name')
            duty_time = data.get('duty_time')
            # 参数校验
            if not all([depart, role, duty_name, duty_time]):
                result['code'] = 1
                result['msg'] = u'参数不完整'
                return jsonify(result)
            # 逻辑处理，入库
            onduty_add = Duty(depart=depart, role=role, duty_name=duty_name, duty_time=duty_time)
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
@blue_watch.route('/duty/<int:duty_id>', methods=['GET', 'PUT', 'DELETE'])
def onduty(duty_id):
    result = {'code': 0, 'data': {}, 'msg': u'查询值班记录成功'}
    duty_change = Duty.query.filter_by(id=duty_id).first()
    if not duty_change:
        result['code'] = 1
        result['msg'] = u'无此值班记录'
        return jsonify(result)
    if request.method == 'GET':
        result['data']['duty_id'] = duty_id
        result['data']['depart'] = duty_change.department_name
        result['data']['role'] = duty_change.role
        result['data']['duty_name'] = duty_change.duty_name
        result['data']['duty_time'] = duty_change.duty_time
        return jsonify(result)
    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            depart = data.get('depart')
            role = data.get('role')
            duty_name = data.get('duty_name')
            duty_time = data.get('duty_time')
            if not all([depart, role, duty_name, duty_time]):
                result['code'] = 1
                result['msg'] = u'参数不完整'
                return jsonify(result)
            duty_change.depart = depart
            duty_change.role_name = role
            duty_change.name = duty_name
            duty_change.duty_time = duty_time
            db.session.commit()
            result['msg'] = u'修改值班记录成功'
            return jsonify(result)
        else:
            result['code'] = 1
            result['msg'] = u'接收不到参数'
            return jsonify(result)
    elif request.method == 'DELETE':
        db.session.delete(duty_change)
        db.session.commit()
        db.session.close()
        result['msg'] = u'已删除此条值班记录'
        return jsonify(result)
