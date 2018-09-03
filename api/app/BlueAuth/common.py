# coding=utf-8
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

# 数据库查询
from app.models import User


def get_table(result=None, table=None, execute=None, id=None, terms=None):
    if execute == 'all':
        try:
            data = table.query.all()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if not data:
            result['code'] = 1
            result['msg'] = u'无数据'
            return result
        return data
    if execute == 'get':
        try:
            data = table.query.get(id)
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if not table:
            result['code'] = 1
            result['msg'] = u'无数据'
            return result
        return data
    if execute == 'first':
        try:
            user = table.query.filter(terms).first()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if user:
            result['code'] = 1
            result['msg'] = u'用户已存在'
            return result


# 接收参数
def accept_para(list):
    para_list = []
    for para in list:
        para = eval(repr(para))
        para = request.json.get(para)
        para_list.append(para)
    return para_list


