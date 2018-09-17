# coding=utf-8

from datetime import datetime, timedelta
import xlwt
from app.models import Duty
from app import db


# 生成excel数据
def data_to_xlsx(filename, *args):
    list_table_head = [u'部门', u'角色', u'日期', u'员工']
    # list_table_head1 = [u'部门', u'部门负责人', '',]
    dateStart = args[0]
    dateEnd = args[1]
    departId = args[2]
    # while dateStart <= dateEnd:
    #     list_table_head1.append(dateStart)
    #     day_date = datetime.strptime(dateStart, '%Y-%m-%d').date()
    #     day_date += timedelta(days=1)
    #     dateStart = day_date.strftime('%Y-%m-%d')
    #     continue
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheetname='data_to_xlsx', cell_overwrite_ok=True)
    # 1 表头第一行写入
    # for i in range(len(list_table_head1)):
    #     sheet.write(0, i, list_table_head1[i])
    # 2 部门-负责人-角色写入
    duty_objs = Duty.query.all()
    row = 1
    for duty_obj in duty_objs:
        # if duty_obj.duty_time.strftime('%Y-%m-%d') in list_table_head1:
        #     sheet.write(row, )
        list1 = [duty_obj.depart, duty_obj.role, duty_obj.duty_time.strftime('%Y-%m-%d'), duty_obj.duty_name]
        for i in range(len(list1)):
            sheet.write(row, i, list1[i])
        row += 1
    workbook.save(filename)
