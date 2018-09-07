# coding=utf-8

from datetime import datetime, timedelta
from collections import defaultdict

from flask import render_template, request, jsonify

from . import blue_watch
from app import db
from app.models import Duty, TempText, Department, Role, User


# 新增单条值班记录
@blue_watch.route('/duty', methods=['POST'])
def duty_add():
    result = {'code': 0, 'msg': u'新增值班记录成功'}
    if request.is_json:
        # 接收参数
        data = request.get_json()
        departId = data.get('departId')
        roleId = data.get('roleId')
        staffId = data.get('staffId')
        date = data.get('date')
        # 参数校验
        if not all([departId, roleId, staffId, date]):
            result['code'] = 1
            result['msg'] = u'参数不完整'
            return jsonify(result)
        # 数据是否存在，时间格式
        try:
            duty_time = datetime.strptime(date, '%Y-%m-%d').date()
            depart = Department.query.filter_by(id=departId, status=1).first().alias
            role = Role.query.filter_by(id=roleId, status=1).first().alias
            user = User.query.filter_by(id=staffId, status=1).first()
        except:
            result['code'] = 1
            result['msg'] = u'参数不正确'
            return jsonify(result)
        duty_name = user.fullname
        mobile = user.mobile
        tag = user.tag
        # 逻辑处理，入库
        dutyAdd = Duty(depart=depart, role=role, duty_name=duty_name, duty_time=duty_time, mobile=mobile, tag=tag)
        result = dutyAdd.add(dutyAdd)
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
    duty_change = Duty.query.filter_by(id=duty_id, status=1).first()
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
            departId = data.get('departId')
            roleId = data.get('roleId')
            staffId = data.get('staffId')
            date = data.get('date')
            if not all([departId, roleId, staffId, date]):
                result['code'] = 1
                result['msg'] = u'参数不完整'
                return jsonify(result)
            # 数据是否存在，时间格式
            try:
                duty_time = datetime.strptime(date, '%Y-%m-%d').date()
                depart = Department.query.filter_by(id=departId, status=1).first().alias
                role = Role.query.filter_by(id=roleId, status=1).first().alias
                user = User.query.filter_by(id=staffId, status=1).first()
            except:
                result['code'] = 1
                result['msg'] = u'参数不正确'
                return jsonify(result)
            duty_name = user.fullname
            mobile = user.mobile
            tag = user.tag
            duty_change.depart = depart
            duty_change.role = role
            duty_change.duty_name = duty_name
            duty_change.duty_time = duty_time
            duty_change.mobile = mobile
            duty_change.tag = tag
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


# 单部门排班数量统计
@blue_watch.route('/dutyStatus', methods=['GET'])
def dutyStatus():
    result = {'code': 1, 'data': {}, 'msg': u'错误'}
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    # 接收参数
    dateRange = data.get('dateRange')
    departId = data.get('departId')
    # 参数校验
    try:
        date_str = str(dateRange).split(',')
    except:
        result['msg'] = u'日期格式不正确'
        return jsonify(result)
    s_time = date_str[0]
    e_time = date_str[1]
    if s_time > e_time:
        result['msg'] = u'日期不合理'
        return jsonify(result)
    depart_obj = Department.query.filter_by(status=1, id=departId).first()
    if not depart_obj:
        result['msg'] = u'部门不存在'
        return jsonify(result)
    s_day = datetime.strptime(s_time, '%Y-%m-%d').date()
    e_day = datetime.strptime(e_time, '%Y-%m-%d').date()
    # 1 日期列表
    dateList = []
    while s_time <= e_time:
        dateList.append(s_time)
        day_date = datetime.strptime(s_time, '%Y-%m-%d').date()
        day_date += timedelta(days=1)
        s_time = day_date.strftime('%Y-%m-%d')
        continue
    result['data']['dateList'] = dateList
    # 2 角色信息
    roleLists = []
    roleList = {}
    role_objs = depart_obj.roles.all()
    for role_obj in role_objs:
        roleLists.append(role_obj.alias)
        roleList[role_obj.alias] = 0
    dutyList = defaultdict(dict)
    # 有记录的值班情况
    duty_objs = Duty.query.filter(Duty.status == 1, Duty.depart == depart_obj.alias, Duty.duty_time.between(s_day, e_day)).all()
    if duty_objs:
        for duty_obj in duty_objs:
            if duty_obj.role in roleList.keys():
                if duty_obj.duty_time.strftime('%Y-%m-%d') in dutyList.keys():
                    if duty_obj.role in dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')].keys():
                        dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role] += 1
                    else:
                        dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role] = 1
                else:
                    dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role] = 1
            else:
                pass
    result['data']['roleList'] = roleLists
    result['data']['dutyList'] = dutyList
    return jsonify(result)
