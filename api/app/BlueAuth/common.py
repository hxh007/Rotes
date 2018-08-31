# coding=utf-8
from flask import request
from sqlalchemy.exc import SQLAlchemyError

# 数据库查询
from app.models import User


def get_database(result=None, database=None, execute=None, id=None):
    if execute == 'all':
        try:
            data = database.query.all()
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
            data = database.query.get(id)
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if not database:
            result['code'] = 1
            result['msg'] = u'无数据'
            return result
        return data

# 接收和校验参数
def accept_verify_para(*args, **kwargs):
    para = []
    for info in request.json:
        pass
