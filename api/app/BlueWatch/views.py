# coding=utf-8

from datetime import datetime, timedelta
from collections import defaultdict
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
import os
from threading import Thread

from flask import render_template, request, jsonify
from flask import send_file, current_app

from . import blue_watch
from app import db
from app.models import Duty, TempText, Department, Role, User
from datas_to_xlsx import data_to_xlsx
from config import Config


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
        date = data.get('dutyDate')
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
            # 部门角色关联关系
            departRoles = Department.query.filter_by(id=departId, status=1).first().roles.all()
            departRole_list = []
            for departRole in departRoles:
                departRole_list.append(departRole.id)
            user = User.query.filter_by(id=staffId, status=1).first()
        except:
            result['code'] = 1
            result['msg'] = u'参数不正确'
            return jsonify(result)
        if not user:
            result['code'] = 1
            result['msg'] = u'无此用户'
            return jsonify(result)
        if roleId not in departRole_list:
            result['code'] = 1
            result['msg'] = u'此部门无此角色'
            return jsonify(result)
        duty_name = user.fullname
        is_duty = Duty.query.filter_by(depart=depart, role=role, duty_time=duty_time, duty_name=duty_name).first()
        if is_duty:
            result['code'] = 1
            result['msg'] = u'已存在此条值班记录'
            return jsonify(result)
        mobile = user.mobile
        ding_id = user.ding_id
        # 逻辑处理，入库
        dutyAdd = Duty(depart=depart, role=role, duty_name=duty_name, duty_time=duty_time, mobile=mobile, ding_id=ding_id)
        result = dutyAdd.add(dutyAdd)
        return jsonify(result)
    else:
        result['code'] = 1
        result['msg'] = u'接收不到参数'
        return jsonify(result)


# 单条值班记录编辑(查询、删除)
@blue_watch.route('/duty/<int:duty_id>', methods=['GET', 'DELETE'])
def duty_edit(duty_id):
    # duty_id  值班记录id
    result = {'code': 0, 'data': {}, 'msg': u'查询值班记录成功'}
    duty_change = Duty.query.filter_by(id=duty_id, status=1).first()
    if not duty_change:
        result['code'] = 1
        result['msg'] = u'无此值班记录'
        return jsonify(result)
    if request.method == 'GET':
        result['data']['dutyId'] = duty_id
        result['data']['departName'] = duty_change.depart
        result['data']['roleName'] = duty_change.role
        result['data']['staffName'] = duty_change.duty_name
        result['data']['dutyDate'] = duty_change.duty_time.strftime("%Y-%m-%d")
        return jsonify(result)
    elif request.method == 'DELETE':
        db.session.delete(duty_change)
        db.session.commit()
        db.session.close()
        result['msg'] = u'已删除此条值班记录'
        return jsonify(result)


# 某天值班记录
@blue_watch.route('/dutyLists', methods=['GET'])
def dutyLists():
    result = {'code': 1, 'data': {}, 'msg': u'参数缺失'}
    # 1 接收参数
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    dateStart = data.get('dateStart')
    dateEnd = data.get('dateEnd')
    departId = data.get('departId')
    # 2 参数校验
    if not all([dateStart, dateEnd]):
        return jsonify(result)
    if dateStart != dateEnd:
        result['msg'] = u'日期不正确'
        return jsonify(result)
    try:
        s_day = datetime.strptime(dateStart, '%Y-%m-%d').date()
        e_day = datetime.strptime(dateEnd, '%Y-%m-%d').date()
    except:
        result['msg'] = u'参数格式不正确'
        return jsonify(result)
    if len(dateStart) != 10 or len(dateEnd) != 10:
        result['msg'] = u'日期格式不规范'
        return jsonify(result)
    # 1 日期
    result['date'] = dateStart
    # 2 值班数据
    data = []
    if departId:
        depart_obj = Department.query.filter_by(id=departId).first()
        if not depart_obj:
            result['msg'] = u'无此部门'
            return jsonify(result)
        # 3 单部门数据返回
        dict_duty = {}
        dict_duty['departId'] = depart_obj.id
        dict_duty['departName'] = depart_obj.alias
        depart_duty_total = Duty.query.filter_by(depart=depart_obj.alias, duty_time=s_day).count()
        dict_duty['total'] = int(depart_duty_total)
        roleList = []
        depart_roles = depart_obj.roles.all()
        if depart_roles:
            for role_obj in depart_roles:
                dict_role = {}
                dict_role['roleId'] = role_obj.id
                dict_role['roleName'] = role_obj.alias
                duty_role_total = Duty.query.filter_by(depart=depart_obj.alias, role=role_obj.alias, duty_time=s_day).count()
                dict_role['total'] = int(duty_role_total)
                duty_lists = Duty.query.filter_by(depart=depart_obj.alias, role=role_obj.alias, duty_time=s_day).all()
                duty_list = []
                if duty_lists:
                    for duty_obj in duty_lists:
                        dict1_duty = {}
                        dict1_duty['dutyId'] = duty_obj.id
                        dict1_duty['dutyName'] = duty_obj.duty_name
                        duty_list.append(dict1_duty)
                dict_role['dutyList'] = duty_list
                roleList.append(dict_role)
        dict_duty['roleList'] = roleList
        data.append(dict_duty)
    else:
        # 4 所有部门值班信息
        # 4.1 部门信息
        depart_objs = Department.query.all()
        if depart_objs:
            for depart_obj in depart_objs:
                dict1 = {}
                dict1['departId'] = depart_obj.id
                dict1['departName'] = depart_obj.alias
                depart_total = Duty.query.filter_by(duty_time=s_day, depart=depart_obj.alias).count()
                dict1['total'] = int(depart_total)
                roleList1 = []
                # 4.2 部门角色信息
                role_objs = depart_obj.roles.all()
                if role_objs:
                    for role_obj in role_objs:
                        dict2 = {}
                        dict2['roleId'] = role_obj.id
                        dict2['roleName'] = role_obj.alias
                        duty_role_total1 = Duty.query.filter_by(duty_time=s_day, depart=depart_obj.alias, role=role_obj.alias).count()
                        dict2['total'] = int(duty_role_total1)
                        dutyList1 = []
                        # 4.3 部门角色值班记录
                        duty_objs = Duty.query.filter_by(duty_time=s_day, depart=depart_obj.alias, role=role_obj.alias).all()
                        if duty_objs:
                            for duty_obj1 in duty_objs:
                                dict3 = {}
                                dict3['dutyId'] = duty_obj1.id
                                dict3['dutyName'] = duty_obj1.duty_name
                                dutyList1.append(dict3)
                        dict2['dutyList'] = dutyList1
                        if dict2['dutyList'] == []:
                            dict1['total'] += 1
                        roleList1.append(dict2)
                dict1['roleList'] = roleList1
                data.append(dict1)
    # 4 返回结果
    result['code'] = 0
    result['msg'] = u'查询值班记录成功'
    result['data'] = data
    return jsonify(result)


# 排班数量统计
@blue_watch.route('/dutysCount', methods=['GET'])
def dutysCount():
    result = {'code': 1, 'data': {}, 'msg': u'统计此部门值班数量成功'}
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    # 1 接收参数
    dateStart = data.get('dateStart')
    dateEnd = data.get('dateEnd')
    departId = data.get('departId')
    # 2 参数校验
    if not all([dateStart, dateEnd]):
        result['msg'] = u'参数缺失'
    if dateStart > dateEnd:
        result['msg'] = u'日期不合理'
        return jsonify(result)
    try:
        datelist = list(rrule(DAILY, dtstart=parse(dateStart), until=parse(dateEnd)))
    except:
        result['msg'] = u'日期格式不正确'
        return jsonify(result)
    s_day = datelist[0].strftime('%Y-%m-%d')
    e_day = datelist[-1].strftime('%Y-%m-%d')
    # 3 日期列表
    dateList = []
    for date_01 in datelist:
        dateList.append(date_01.strftime('%Y-%m-%d'))
    result['data']['dateList'] = dateList
    # 4 单部门
    if departId:
        depart_obj = Department.query.filter_by(status=1, id=departId).first()
        if not depart_obj:
            result['msg'] = u'部门不存在'
            return jsonify(result)
        # 4.1 部门信息
        departInfo = {}
        departInfo[depart_obj.id] = depart_obj.alias
        result['data']['dapartInfo'] = departInfo
        # 4.2 部门角色信息
        roleList = {}
        roleLists = {}
        role_objs = depart_obj.roles.all()
        if role_objs:
            for role_obj in role_objs:
                roleLists[role_obj.id] = role_obj.alias
                roleList[role_obj.alias] = 0
        result['data']['departRoles'] = roleLists
        dutyList = defaultdict(dict)
        # 4.3 有记录的值班情况
        duty_objs = Duty.query.filter(Duty.status == 1, Duty.depart == depart_obj.alias,
                                      Duty.duty_time.between(s_day, e_day)).all()
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
        result['data']['dutyList'] = dutyList
        result['code'] = 0
        return jsonify(result)
    # 5 全部门
    # 5.1 部门角色信息
    """{部门id: {角色id: 角色名},}"""
    departList = {}
    depart_roles = defaultdict(dict)
    depart_objs = Department.query.all()
    if depart_objs:
        for depart_obj in depart_objs:
            departList[depart_obj.id] = depart_obj.alias
            role_objs = depart_obj.roles.all()
            if role_objs:
                for role_obj in role_objs:
                    depart_roles[depart_obj.id][role_obj.id] = role_obj.alias
    result['data']['departInfo'] = departList
    result['data']['departRoles'] = depart_roles
    # 5.2 值班统计信息
    dutyLists = defaultdict(dict)
    duty_objs = Duty.query.filter(Duty.status == 1, Duty.duty_time.between(s_day, e_day)).all()
    if duty_objs:
        for duty_obj in duty_objs:
            # 先判断时间
            if duty_obj.duty_time.strftime("%Y-%m-%d") in dutyLists.keys():
                # 判断部门名
                if duty_obj.depart in dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")].keys():
                    # 判断角色名
                    if duty_obj.role in dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart].keys():
                        # 存在则数量+1
                        dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role] += 1
                    else:
                        dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role] = 1
                else:
                    dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role] = 1
            else:
                dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")] = defaultdict(dict)
                dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role] = 1
    result['data']['dutyList'] = dutyLists
    result['code'] = 0
    result['msg'] = u'统计所有部门值班数量成功'
    return jsonify(result)


# 值班记录
@blue_watch.route('/dutys', methods=['GET'])
def dutys():
    result = {'code': 1, 'data': {}, 'msg': u'此部门值班记录'}
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    # 1 接收参数
    dateStart = data.get('dateStart')
    dateEnd = data.get('dateEnd')
    departId = data.get('departId')
    # 2 参数校验
    if not all([dateStart, dateEnd]):
        result['msg'] = u'参数缺失'
    if dateStart > dateEnd:
        result['msg'] = u'日期不合理'
        return jsonify(result)
    try:
        datelist = list(rrule(DAILY, dtstart=parse(dateStart), until=parse(dateEnd)))
    except:
        result['msg'] = u'日期格式不正确'
        return jsonify(result)
    s_day = datelist[0].strftime('%Y-%m-%d')
    e_day = datelist[-1].strftime('%Y-%m-%d')
    # 3 日期列表
    dateList = []
    for date_01 in datelist:
        dateList.append(date_01.strftime('%Y-%m-%d'))
    result['data']['dateList'] = dateList
    # 4 单部门
    if departId:
        depart_obj = Department.query.filter_by(status=1, id=departId).first()
        if not depart_obj:
            result['msg'] = u'部门不存在'
            return jsonify(result)
        # 4.1 部门及负责人信息
        departInfo = defaultdict(dict)
        # 4.2 部门负责人
        is_depart_objs = depart_obj.users.all()
        is_depart_list = []
        if is_depart_objs:
            for is_depart_obj in is_depart_objs:
                if is_depart_obj.is_department:
                    is_depart_list.append(is_depart_obj.fullname)
        departInfo[depart_obj.id][depart_obj.alias] = is_depart_list
        result['data']['dapartInfo'] = departInfo
        # 4.3 部门角色信息
        roleList = {}
        roleLists = {}
        role_objs = depart_obj.roles.all()
        if role_objs:
            for role_obj in role_objs:
                roleLists[role_obj.id] = role_obj.alias
                roleList[role_obj.alias] = 0
        result['data']['departRoles'] = roleLists
        dutyList = defaultdict(dict)
        # 4.3 有记录的值班情况
        duty_objs = Duty.query.filter(Duty.status == 1, Duty.depart == depart_obj.alias,
                                      Duty.duty_time.between(s_day, e_day)).all()
        if duty_objs:
            for duty_obj in duty_objs:
                if duty_obj.role in roleList.keys():
                    if duty_obj.duty_time.strftime('%Y-%m-%d') in dutyList.keys():
                        if duty_obj.role in dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')].keys():
                            dutyList[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.role][duty_obj.id] = duty_obj.duty_name
                            dutyList[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.role]['count'] += 1
                        else:
                            dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role][duty_obj.id] = duty_obj.duty_name
                            dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role]['count'] = 1
                    else:
                        dutyList[duty_obj.duty_time.strftime("%Y-%m-%d")] = defaultdict(dict)
                        dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role][duty_obj.id] = duty_obj.duty_name
                        dutyList[duty_obj.duty_time.strftime('%Y-%m-%d')][duty_obj.role]['count'] = 1
                else:
                    pass
        result['data']['dutyList'] = dutyList
        result['code'] = 0
        return jsonify(result)
    # 5 全部门
    # 5.1 部门及负责人信息
    # 5.2 部门角色关系信息
    """{部门id: {部门名: [负责人名字列表]},}
        {部门id: {角色id: 角色名},}"""
    departList = defaultdict(dict)
    depart_roles = defaultdict(dict)
    depart_objs = Department.query.all()
    if depart_objs:
        for depart_obj in depart_objs:
            # 部门负责人
            is_depart_objs = depart_obj.users.all()
            is_depart_list = []
            if is_depart_objs:
                for is_depart_obj in is_depart_objs:
                    if is_depart_obj.is_department:
                        is_depart_list.append(is_depart_obj.fullname)
            departList[depart_obj.id][depart_obj.alias] = is_depart_list
            # 部门角色关系
            role_objs = depart_obj.roles.all()
            if role_objs:
                for role_obj in role_objs:
                    depart_roles[depart_obj.id][role_obj.id] = role_obj.alias
    result['data']['departInfo'] = departList
    result['data']['departRoles'] = depart_roles
    # 5.2 值班统计信息
    dutyLists = defaultdict(dict)
    duty_objs = Duty.query.filter(Duty.status == 1, Duty.duty_time.between(s_day, e_day)).all()
    if duty_objs:
        for duty_obj in duty_objs:
            # 先判断时间
            if duty_obj.duty_time.strftime("%Y-%m-%d") in dutyLists.keys():
                # 判断部门名
                if duty_obj.depart in dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")].keys():
                    # 判断角色名
                    if duty_obj.role in dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart].keys():
                        # 存在则数量+1
                        dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][
                            duty_obj.id] = duty_obj.duty_name+duty_obj.mobile
                        # count
                        dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][
                            'count'] += 1
                    else:
                        dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][
                            duty_obj.id] = duty_obj.duty_name+duty_obj.mobile
                        # count
                        dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][
                            'count'] = 1
                else:
                    dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart] = defaultdict(dict)
                    dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][
                        duty_obj.id] = duty_obj.duty_name+duty_obj.mobile
                    # count
                    dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][
                        'count'] = 1
            else:
                dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")] = defaultdict(dict)
                dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart] = defaultdict(dict)
                dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role][duty_obj.id] = duty_obj.duty_name+duty_obj.mobile
                # count
                dutyLists[duty_obj.duty_time.strftime("%Y-%m-%d")][duty_obj.depart][duty_obj.role]['count'] = 1
    result['data']['dutyList'] = dutyLists
    result['code'] = 0
    result['msg'] = u'所有部门值班记录'
    return jsonify(result)


# 编辑短信内容模板
@blue_watch.route('/tempContent', methods=['GET', 'PUT', 'DELETE'])
def smsTemplate():
    result = {'code': 0, 'data': {}, 'msg': u'暂无模板数据'}
    if request.method == 'GET':
        try:
            tempContent = TempText.query.filter_by(name='SMS').first().content
        except:
            return jsonify(result)
        result['data']['tempContent'] = tempContent
        result['msg'] = u'查询模板数据成功'
        return jsonify(result)
    if request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.values
        tempContent = data.get('tempContent')
        if not tempContent:
            result['code'] = 1
            result['msg'] = u'内容不能为空'
            return jsonify(result)
        try:
            # 修改模板内容
            temp_obj = TempText.query.filter_by(name='SMS').first()
            temp_obj.content = tempContent
            result1 = temp_obj.add(temp_obj)
        except:
            # 新增
            temp_obj = TempText(name='SMS', content=tempContent)
            result1 = temp_obj.add(temp_obj)
        return jsonify(result1)
    if request.method == 'DELETE':
        try:
            temp_obj = TempText.query.filter_by(name='SMS').first()
            db.session.delete(temp_obj)
            db.session.commit()
            result['msg'] = u'删除成功'
        except:
            result['code'] = 1
            result['msg'] = u'删除失败'
        return jsonify(result)


# 转为Excel文件
@blue_watch.route('/datatoxlsx', methods=['POST'])
def xlsx():
    result = {'code': 1, 'msg': u'正在生成Excel文件'}
    # 1 接收参数
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    dateStart = data.get('dateStart')
    dateEnd = data.get('dateEnd')
    # 2 参数校验
    if not all([dateStart, dateEnd]):
        result['msg'] = u'参数缺失'
        return jsonify(result)
    if dateStart > dateEnd:
        result['msg'] = u'日期不合理'
        return jsonify(result)
    try:
        dateList = list(rrule(DAILY, dtstart=parse(dateStart), until=parse(dateEnd)))
    except:
        result['msg'] = u'日期格式不正确'
        return jsonify(result)
    # 3 调用生成excel函数
    Excel_filename = os.path.join(Config.Excel_path, dateStart+'_' + dateEnd + '.xlsx')
    # 子线程
    to_xlsx = Thread(target=data_to_xlsx, args=(Excel_filename, dateList, current_app._get_current_object()))
    to_xlsx.start()
    result['data'] = dateStart+'_' + dateEnd + '.xlsx'
    return jsonify(result)


# 发送Excel文件
@blue_watch.route('/sendxlsx', methods=['POST'])
def send_xlsx():
    result = {'code': 1, 'msg': u'参数缺失'}
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    fileName = data.get('fileName')
    if not fileName:
        return jsonify(result)
    fileName1 = str(fileName)
    try:
        result1 = send_file('static/' + fileName1, as_attachment=True)
        return result1
    except:
        result['msg'] = u'正在生成Excel文件'
        return jsonify(result)
