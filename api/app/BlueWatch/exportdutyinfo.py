# coding=utf-8
from collections import defaultdict

from app.models import Duty, Department


def exportdutyinfo(dateList, capp):
    with capp.app_context():
        # 函数返回的数据格式
        dataResult = {}
        # 1 日期列表
        list_table_head = []
        s_day = dateList[0].strftime('%Y-%m-%d')
        e_day = dateList[-1].strftime('%Y-%m-%d')
        for datedate in dateList:
            list_table_head.append(datedate.strftime('%Y-%m-%d'))
        dataResult['dateList'] = list_table_head
        # 2 部门、负责人、角色关系整理
        depart_objs = Department.query.filter_by(status=1).all()
        departInfo = {}
        departRoles = {}
        if depart_objs:
            for depart_obj in depart_objs:
                # 负责人
                is_depart_objs = depart_obj.users.all()
                is_depart_list = []
                if is_depart_objs:
                    for is_depart_obj in is_depart_objs:
                        if is_depart_obj.is_department:
                            is_depart_list.append(is_depart_obj.fullname)
                departInfo[depart_obj.alias] = is_depart_list
                # 角色
                role_objs = depart_obj.roles.all()
                role_list = []
                if role_objs:
                    for role_obj in role_objs:
                        role_list.append(role_obj.alias)
                departRoles[depart_obj.alias] = role_list
        # 3 整理出排班模型数据
        dutyInfo = defaultdict(dict)
        duty_objs = Duty.query.filter(Duty.duty_time.between(s_day, e_day)).all()
        # 3.1 有记录的
        if duty_objs:
            for duty_obj in duty_objs:
                # 部门角色在的
                if duty_obj.depart in departRoles.keys() and duty_obj.role in departRoles[duty_obj.depart]:
                    # 判部门
                    if duty_obj.depart in dutyInfo.keys():
                        # 判角色
                        if duty_obj.role in dutyInfo[duty_obj.depart].keys():
                            # 判时间
                            if duty_obj.duty_time.strftime('%Y-%m-%d') in dutyInfo[duty_obj.depart][duty_obj.role].keys():
                                dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')].append(
                                    duty_obj.duty_name + duty_obj.mobile)
                            else:
                                dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')] = [
                                    duty_obj.duty_name + duty_obj.mobile]
                        else:
                            dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')] = [
                                duty_obj.duty_name + duty_obj.mobile]
                    else:
                        dutyInfo[duty_obj.depart] = defaultdict(dict)
                        dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')] = [
                            duty_obj.duty_name + duty_obj.mobile]
        # 3.2 没部门记录的
        departs_lose_list = list(set(departRoles.keys()) - set(dutyInfo.keys()))
        if departs_lose_list:
            for depart_list in departs_lose_list:
                dutyInfo[depart_list] = {}
                for role_name in departRoles[depart_list]:
                    dutyInfo[depart_list][role_name] = {}
        # 3.3 有部门没角色记录的
        for depart_lose_name in dutyInfo.keys():
            role_quan = set(departRoles[depart_lose_name])
            role_lose = set(dutyInfo[depart_lose_name].keys())
            depart_roles_lose = list(role_quan - role_lose)
            for depart_role_lose in depart_roles_lose:
                dutyInfo[depart_lose_name][depart_role_lose] = {}
        # 3.4 数量统计及负责人插入
        for depart_lose_name in dutyInfo.keys():
            depart_count = 1
            role_lists = dutyInfo[depart_lose_name].keys()
            if role_lists:
                depart_count = 0
                for role_list in role_lists:
                    date_values_list = dutyInfo[depart_lose_name][role_list].values()
                    list1 = map(lambda l: len(l), date_values_list)
                    try:
                        count = max(list1)
                    except:
                        count = 1
                    dutyInfo[depart_lose_name][role_list]['count'] = count
                    depart_count += dutyInfo[depart_lose_name][role_list]['count']
            dutyInfo[depart_lose_name]['count'] = depart_count
            dutyInfo[depart_lose_name]['managerList'] = departInfo[depart_lose_name]
        dataResult['dutyInfo'] = dutyInfo
        return dataResult