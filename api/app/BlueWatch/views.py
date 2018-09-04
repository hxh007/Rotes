# coding=utf-8

from datetime import datetime, timedelta

from flask import render_template, request, jsonify

from . import blue_watch
from app import db
from app.models import Duty, TempText, Department, tb_department_role


# 新增单条值班记录
@blue_watch.route('/duty', methods=['POST'])
def duty_add():
    result = {'code': 0, 'msg': u'新增值班记录成功'}
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
        # 时间格式
        try:
            duty_ctime = datetime.strptime(duty_time, '%Y-%m-%d').date()
        except:
            result['code'] = 1
            result['msg'] = u'时间格式不正确'
            return jsonify(result)
        # 逻辑处理，入库
        onduty_add = Duty(depart=depart, role=role, duty_name=duty_name, duty_time=duty_ctime)
        result = onduty_add.add(onduty_add)
        return jsonify(result)
    else:
        result['code'] = 1
        result['msg'] = u'接收不到参数'
        return jsonify(result)


# 单条值班记录编辑
@blue_watch.route('/duty/<int:duty_id>', methods=['GET', 'PUT', 'DELETE'])
def duty_edit(duty_id):
    # duty_id  值班记录id
    result = {'code': 0, 'data': {}, 'msg': u'查询值班记录成功'}
    duty_change = Duty.query.filter_by(id=duty_id).first()
    if not duty_change:
        result['code'] = 1
        result['msg'] = u'无此值班记录'
        return jsonify(result)
    if request.method == 'GET':
        result['data']['duty_id'] = duty_id
        result['data']['depart'] = duty_change.depart
        result['data']['role'] = duty_change.role
        result['data']['duty_name'] = duty_change.duty_name
        result['data']['duty_time'] = duty_change.duty_time.strftime("%Y-%m-%d")
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
            # 时间格式
            try:
                duty_ctime = datetime.strptime(duty_time, '%Y-%m-%d').date()
            except:
                result['code'] = 1
                result['msg'] = u'时间格式不正确'
                return jsonify(result)
            duty_change.depart = depart
            duty_change.role = role
            duty_change.duty_name = duty_name
            duty_change.duty_time = duty_ctime
            result = duty_change.add(duty_change)
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


# 单部门值班记录列表
@blue_watch.route('/dutys/<int:depart_id>', methods=['GET', 'POST'])
def duty_depart(depart_id):
    # 默认返回本月的，也可以指定上个月、下个月
    result = {'code': 0, 'data': {}, 'msg': u'查询此部门值班记录列表成功'}
    # 部门id校验
    try:
        depart_alias = Department.query.filter_by(id=depart_id).first().alias
    except:
        result['code'] = 1
        result['msg'] = u'无此部门'
        return jsonify(result)
    # 接收参数
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    result['data']['depart'] = depart_alias
    if not data:
        # 不传参数，默认返回本月的
        today = datetime.today().date()
        month = today.month
        if today.month == 12:
            month = 0
        # 本月第一天
        month_first = datetime(today.year, today.month, 1).date()
        future_mouth_first = datetime(today.year, month+1, 1)
        # 本月最后一天
        this_month_last = (future_mouth_first - timedelta(days=1)).date()
        # 1 角色列表
        role_lists = Department.query.filter_by(id=depart_id).first().roles
        if role_lists:
            for role_list in role_lists:
                # todo 遍历角色表获取角色名
                pass

        departs = Duty.query.filter(Duty.depart == depart_alias, Duty.duty_time.between(month_first, this_month_last)).all()
        role_list = []
        for depart in departs:
            if depart.role in role_list:
                pass
            else:
                role_list.append(depart.role)
        result['data']['role_list'] = role_list
        return jsonify(result)

        pass
    elif data and data.get('Month') == 'Before':
        # 返回上个月的
        pass
    elif data and data.get('Month') == 'Next':
        # 返回下个月的
        pass
    else:
        # 报错
        pass


# 查询所有部门排班记录列表
@blue_watch.route('/dutyList', methods=['GET', 'POST'])
def dutyList():
    # 默认返回本月的，也可以指定日期范围返回
    pass