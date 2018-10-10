# coding=utf-8

from io import BytesIO
import xlsxwriter

from app.models import Duty, Department
from exportdutyinfo import exportdutyinfo


# 生成excel数据
def data_to_xlsx(filename, dateList, capp):
    with capp.app_context():
        # 1 整理获得的数据
        dataResult = exportdutyinfo(dateList, capp)
        dateList = dataResult['dateList']
        dutyInfo = dataResult['dutyInfo']
        list_table_head = [u'部门', u'部门负责人', u'角色', ]
        list_table_head.extend(dateList)
        # 2 写入信息
        output = BytesIO()
        output.name = filename
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(u'值班表')
        # 文本换行格式
        merge_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'color': '#000000',
        })
        merge_format.set_text_wrap()
        # 第一行格式
        merge_format1 = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'color': '#000000',
        })
        # 3 表头第一行写入
        for i in range(len(list_table_head)):
            sheet.write(0, i, list_table_head[i], merge_format1)
        # # 4 第二行，值班总监，三线值班
        sheet.merge_range(1, 0, 1, 2, u'值班总监', merge_format)
        sheet.merge_range(2, 0, 2, 2, u'三线值班', merge_format)
        row_depart = 1
        tf_alias = Department.query.filter_by(name='MODULE_TF').first().alias
        tf_roles_list = filter(lambda x: x not in ['count', 'managerList'], dutyInfo[tf_alias].keys())
        if tf_roles_list:
            for os_role in tf_roles_list:
                if os_role == u'四线值班':
                    sheet.merge_range(1, 0, 1, 2, u'值班总监', merge_format)
                    date_list2 = filter(lambda x: x != 'count', dutyInfo[tf_alias][os_role].keys())
                    for date_day in date_list2:
                        # 日期列数
                        date_line = list_table_head.index(date_day)
                        # 当天值班人列表
                        duty_names = dutyInfo[tf_alias][os_role][date_day]
                        for duty_namer in duty_names:
                            # 3 写入值班人
                            sheet.write(row_depart, date_line, duty_namer)
                elif os_role == u'三线值班':
                    sheet.merge_range(2, 0, 2, 2, u'三线值班', merge_format)
                    date_list2 = filter(lambda x: x != 'count', dutyInfo[tf_alias][os_role].keys())
                    for date_day in date_list2:
                        # 日期列数
                        date_line = list_table_head.index(date_day)
                        # 当天值班人列表
                        duty_names = dutyInfo[tf_alias][os_role][date_day]
                        for duty_namer in duty_names:
                            # 3 写入值班人
                            sheet.write(row_depart, date_line, duty_namer)
                row_depart += 1
        # 清除三四线部门
        dutyInfo.pop(tf_alias)
        row_depart = 3
        # 5.1 写入系统运维部、网络安全部的信息
        op_alias = Department.query.filter_by(name='MODULE_OP').first().alias
        sec_alias = Department.query.filter_by(name='MODULE_SEC').first().alias
        op_sec_list = [op_alias, sec_alias]
        for op_sec in op_sec_list:
            # 5.2 部门负责人，数量
            op_sec_depart = ','.join(dutyInfo[op_sec]['managerList'])
            op_sec_count = dutyInfo[op_sec]['count']
            for os_i in range(op_sec_count):
                # 5.3 部门名，负责人
                sheet.write(row_depart + os_i, 0, op_sec)
                sheet.write(row_depart + os_i, 1, op_sec_depart)
            # 5.4 合并部门单元格
            if op_sec_count == 1:
                sheet.write(row_depart, 0, op_sec, merge_format)
                sheet.write(row_depart, 1, op_sec_depart, merge_format)
            else:
                sheet.merge_range(row_depart, 0, row_depart + op_sec_count - 1, 0, op_sec, merge_format)
                sheet.merge_range(row_depart, 1, row_depart + op_sec_count - 1, 1, op_sec_depart, merge_format)
            os_roles_list = filter(lambda x: x not in ['count', 'managerList'], dutyInfo[op_sec].keys())
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
                        sheet.merge_range(row_depart, 2, row_depart + role_count - 1, 2, os_role, merge_format)
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
                sheet.write(row_depart + i, 0, depart_name)
                # 写入负责人
                sheet.write(row_depart + i, 1, ','.join(dutyInfo[depart_name]['managerList']))
            # 6.2 合并部门单元格
            if depart_counts == 1:
                sheet.write(row_depart, 0, depart_name, merge_format)
                sheet.write(row_depart, 1, ','.join(dutyInfo[depart_name]['managerList']), merge_format)
            else:
                pass
                sheet.merge_range(row_depart, 0, row_depart + depart_counts - 1, 0, depart_name, merge_format)
                sheet.merge_range(row_depart, 1, row_depart + depart_counts - 1, 1, ','.join(dutyInfo[depart_name]['managerList']),
                                  merge_format)
            # 6.3 角色信息写入
            list2 = role_name.keys()
            roleInfo = filter(lambda x: x not in ['count', 'managerList'], list2)
            if roleInfo:
                for role1 in roleInfo:
                    # 此角色写入的行数
                    count1 = dutyInfo[depart_name][role1]['count']
                    # 值班日期列表
                    date_list1 = role_name[role1].keys()
                    date_list2 = filter(lambda x: x != 'count', date_list1)
                    for i1 in range(count1):
                        # 写入角色名
                        sheet.write(row_depart + i1, 2, role1)
                    # 6.4 合并角色单元格
                    if count1 == 1:
                        sheet.write(row_depart, 2, role1, merge_format)
                    else:
                        sheet.merge_range(row_depart, 2, row_depart + count1 - 1, 2, role1, merge_format)
                    for date_day in date_list2:
                        # 日期列数
                        date_line = list_table_head.index(date_day)
                        # 当天值班人列表
                        duty_names = role_name[role1][date_day]
                        for duty_namer in duty_names:
                            # 6.5 写入值班人
                            sheet.write(row_depart + duty_names.index(duty_namer), date_line, duty_namer)
                    row_depart += count1
            else:
                row_depart += depart_counts
        sheet.set_column(0, 2, 13)
        sheet.set_column(3, len(list_table_head)-1, 18)
        workbook.close()
        output.seek(0)
        return output
