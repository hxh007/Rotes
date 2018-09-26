# coding=utf-8

from collections import defaultdict
import xlsxwriter

from app.models import Duty, Department


# 生成excel数据
def data_to_xlsx(filename, dateList, capp):
    with capp.app_context():
        list_table_head = [u'部门', u'部门负责人', u'角色',]
        s_day = dateList[0].strftime('%Y-%m-%d')
        e_day = dateList[-1].strftime('%Y-%m-%d')
        for datedate in dateList:
            list_table_head.append(datedate.strftime('%Y-%m-%d'))
        workbook = xlsxwriter.Workbook(filename)
        sheet = workbook.add_worksheet()
        merge_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'color': '#000000',
        })
        # 1 表头第一行写入
        for i in range(len(list_table_head)):
            sheet.write(0, i, list_table_head[i], merge_format)
        # # 2 第二行，值班总监，三线值班
        sheet.merge_range(1, 0, 1, 2, u'值班总监', merge_format)
        sheet.merge_range(2, 0, 2, 2, u'三线值班', merge_format)
        # 3 部门及负责人及角色关系
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
        # 4 整理出排班模型数据
        dutyInfo = defaultdict(dict)
        duty_objs = Duty.query.filter(Duty.duty_time.between(s_day, e_day)).all()
        # 4.1 有记录的
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
                                dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')].append(duty_obj.duty_name + duty_obj.mobile)
                            else:
                                dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')] = [
                                    duty_obj.duty_name + duty_obj.mobile]
                        else:
                            dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')] = [duty_obj.duty_name + duty_obj.mobile]
                    else:
                        dutyInfo[duty_obj.depart] = defaultdict(dict)
                        dutyInfo[duty_obj.depart][duty_obj.role][duty_obj.duty_time.strftime('%Y-%m-%d')] = [duty_obj.duty_name + duty_obj.mobile]
        # 4.2 没部门记录的
        departs_lose_list = list(set(departRoles.keys()) - set(dutyInfo.keys()))
        if departs_lose_list:
            for depart_list in departs_lose_list:
                dutyInfo[depart_list] = {}
                for role_name in departRoles[depart_list]:
                    dutyInfo[depart_list][role_name] = {}
        # 4.3 有部门没角色记录的
        for depart_lose_name in dutyInfo.keys():
            role_quan = set(departRoles[depart_lose_name])
            role_lose = set(dutyInfo[depart_lose_name].keys())
            depart_roles_lose = list(role_quan-role_lose)
            for depart_role_lose in depart_roles_lose:
                dutyInfo[depart_lose_name][depart_role_lose] = {}
        # 每个角色最大数量统计
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
        # 5 写入整理的数据
        # 第几行
        row_depart = 3
        # 5.1 写入系统运维部、网络安全部的信息
        op_alias = Department.query.filter_by(name='MODULE_OP').first().alias
        sec_alias = Department.query.filter_by(name='MODULE_SEC').first().alias
        op_sec_list = [op_alias, sec_alias]
        for op_sec in op_sec_list:
            # 5.2 部门负责人，数量
            op_sec_depart = ','.join(departInfo[op_sec])
            op_sec_count = dutyInfo[op_sec]['count']
            for os_i in range(op_sec_count):
                # 5.3 部门名，负责人
                sheet.write(row_depart+os_i, 0, op_sec)
                sheet.write(row_depart+os_i, 1, op_sec_depart)
            # 5.4 合并部门单元格
            if op_sec_count == 1:
                sheet.write(row_depart, 0, op_sec, merge_format)
                sheet.write(row_depart, 1, op_sec_depart, merge_format)
            else:
                sheet.merge_range(row_depart, 0, row_depart+op_sec_count-1, 0, op_sec, merge_format)
                sheet.merge_range(row_depart, 1, row_depart+op_sec_count-1, 1, op_sec_depart, merge_format)
            os_roles_list = filter(lambda x: x != 'count', dutyInfo[op_sec].keys())
            # 5.5 写角色信息
            if os_roles_list:
                for os_role in os_roles_list:
                    role_count = dutyInfo[op_sec][os_role]['count']
                    for role_i1 in range(role_count):
                        # 写入角色名
                        sheet.write(row_depart + role_i1, 2, os_role)
                    # 5.6 合并角色单元格
                    if role_count == 1:
                        sheet.write(row_depart, 2, os_role, merge_format)
                    else:
                        sheet.merge_range(row_depart, 2, row_depart + role_count-1, 2, os_role, merge_format)
                    # 5.7 值班日期列表
                    date_list1 = dutyInfo[op_sec][os_role].keys()
                    date_list2 = filter(lambda x: x != 'count', date_list1)
                    for date_day in date_list2:
                        # 日期列数
                        date_line = list_table_head.index(date_day)
                        # 当天值班人列表
                        duty_names = dutyInfo[op_sec][os_role][date_day]
                        for duty_namer in duty_names:
                            # 3 写入值班人
                            sheet.write(row_depart + duty_names.index(duty_namer), date_line, duty_namer)
                    row_depart += role_count
            else:
                row_depart += op_sec_count
            # 清除两个部门
            dutyInfo.pop(op_sec)
        # 6 其他部门的
        for depart_name, role_name in dutyInfo.items():
            # 6.1 部门信息写多少行
            depart_counts = dutyInfo[depart_name]['count']
            for i in range(depart_counts):
                # 写入部门名
                sheet.write(row_depart+i, 0, depart_name)
                # 写入负责人
                sheet.write(row_depart+i, 1, ','.join(departInfo[depart_name]))
            # 6.2 合并部门单元格
            if depart_counts == 1:
                sheet.write(row_depart, 0, depart_name, merge_format)
                sheet.write(row_depart, 1, ','.join(departInfo[depart_name]), merge_format)
            else:
                pass
                sheet.merge_range(row_depart, 0, row_depart+depart_counts-1, 0, depart_name, merge_format)
                sheet.merge_range(row_depart, 1, row_depart+depart_counts-1, 1, ','.join(departInfo[depart_name]), merge_format)
            # 6.3 角色信息写入
            list2 = role_name.keys()
            roleInfo = filter(lambda x: x != 'count', list2)
            if roleInfo:
                for role1 in roleInfo:
                    # 此角色写入的行数
                    count1 = dutyInfo[depart_name][role1]['count']
                    # 值班日期列表
                    date_list1 = role_name[role1].keys()
                    date_list2 = filter(lambda x: x != 'count', date_list1)
                    for i1 in range(count1):
                        # 写入角色名
                        sheet.write(row_depart+i1, 2, role1)
                    # 6.4 合并角色单元格
                    if count1 == 1:
                        sheet.write(row_depart, 2, role1, merge_format)
                    else:
                        pass
                        sheet.merge_range(row_depart, 2, row_depart + count1-1, 2, role1, merge_format)
                    for date_day in date_list2:
                        # 日期列数
                        date_line = list_table_head.index(date_day)
                        # 当天值班人列表
                        duty_names = role_name[role1][date_day]
                        for duty_namer in duty_names:
                            # 6.5 写入值班人
                            sheet.write(row_depart+duty_names.index(duty_namer), date_line, duty_namer)
                    row_depart += count1
            else:
                row_depart += depart_counts
        workbook.close()
