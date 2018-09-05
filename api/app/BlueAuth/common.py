# coding=utf-8

from flask import request
from sqlalchemy.exc import SQLAlchemyError


# 数据库查询
def get_table(result=None, table=None, execute=None, id=None, terms=None, relationship=None):
    # 查询所有
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
    # id查询
    if execute == 'get':
        try:
            data = table.query.get(id)
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if not data:
            result['code'] = 1
            result['msg'] = u'无数据'
            return result
        return data
    # 条件查询
    if execute == 'first':
        try:
            data = table.query.filter(terms).first()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if data:
            result['code'] = 1
            result['msg'] = u'数据已存在'
            return result
        return data
    # 字段查询
    if execute == 'with_entities':
        try:
            data = table.query.with_entities(terms).all()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if not data:
            result['code'] = 1
            result['msg'] = u'数据不存在'
            return result
        return data
    # 表关系查询
    if execute == 'relationship':
        try:
            data = relationship
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        return data


# 接收参数
def accept_para(list):
    para_list = []
    for para in list:
        para = eval(repr(para))
        para = request.json.get(para)
        para_list.append(para)
    return para_list
