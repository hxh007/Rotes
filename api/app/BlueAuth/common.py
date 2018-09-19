# coding=utf-8

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.models import Department, User, Role, Management, Permission

# 数据库查询
def get_table(result=None, table=None, execute=None, id=None, terms=None, relationship=None, page=None, per_page=None):
    # 查询所有
    if execute == 'all':
        try:
            data = table.query.all()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        if not data:
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
            data = relationship.all()
        except SQLAlchemyError:
            result['code'] = 1
            result['msg'] = u'数据查询失败'
            return result
        return data
    # 分页查询
    if execute == 'paginate':
        if int(per_page) >= 30:
            per_page = 30
        pagination = table.query.order_by(terms).paginate(page, per_page=per_page, error_out=False)
        if not pagination.total:
            result['code'] = 0
            result['msg'] = u'无数据'
            return result
        return pagination


# 接收参数
def accept_para(list):
    para_list = []
    for para in list:
        para = eval(repr(para))
        para = request.json.get(para)
        para_list.append(para)
    return para_list


# 响应
def response_return(code=None, msg=None, data=None, managerList=None):
    return {
        'code': code,
        'data': data,
        'managerList': managerList,
        'msg' : msg
    }


# 查询关系类型
class TableTelationType:
    # 部门和用户多对多关系
    DU = 1
    # 部门和角色多对多关系
    DR = 2
    # 管理组和用户多对多关系
    MU = 3
    # 管理组和权限多对多关系
    MP = 4
    genre = {
        DU: {'f_table': Department,
             's_table': User
        },
        DR: {'f_table': Department,
             's_table': Role
        },
        MU: {'f_table': Management,
             's_table': User
        },
        MP: {'f_table': Management,
             's_table': Permission
        }
    }
