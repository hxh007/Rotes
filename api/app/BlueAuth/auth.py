# coding=utf-8
import functools

import jwt, datetime
from flask import jsonify, request, g

import config
from app import Redis
from app.BlueAuth.common import response_return, get_table
from app.models import User, Management, Department
from .constants import JWT_EXP_DAYS, JWT_EXP_SECONDS

class Authentication():

    @staticmethod
    def encode_jwt_token(user):
        '''
        生成认证Token
        :return:jwt_token
        '''
        try:
            managerList = map(lambda m:m.name, user.u_managements.all())
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_SECONDS), # 过期时间
                'iat': datetime.datetime.utcnow(), # 签发时间
                'iss': 'auth', # 签发人
                'data':{
                    'id': user.id,
                    'username': user.username,
                    'managerList': managerList,
                    'login_time': user.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'lastchange': user.lastchange.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            return jwt.encode(
                payload,
                config.Config.SECRET_KEY,
                algorithm='HS256'
                )
        except Exception:
            return response_return(1, u'生成token失败')

    @staticmethod
    def decode_jwt_token(jwt_token):
        '''
        验证token
        :param auth_token: jwt_token
        :return:用户信息
        '''
        try:
            payload = jwt.decode(jwt_token, config.Config.SECRET_KEY)
            if ('data' in payload and 'id' in payload['data']):
                return response_return(0, data=payload)
            else:
                return response_return(2, u'无效token')
        except Exception:
            return response_return(2, u'无效token')

    @staticmethod
    def set_redis_jwt(user_mobile, jwt_token):
        '''
        把jwt_token保存到redis中
        '''
        try:
            Redis.setex('jwt_' + user_mobile, JWT_EXP_SECONDS, jwt_token)
        except Exception:
            return response_return(1, u'jwt_token保存失败')

    @staticmethod
    def get_redis_jwt(self, user_mobile):
        '''
        获取redis中的jwt_token
        '''
        try:
            jwt_token = Redis.get('jwt_' + user_mobile)
            payload = self.decode_jwt_token(jwt_token)
        except Exception:
            return u'获取jwt_token失败'
        return payload

    @staticmethod
    def del_redis_jwt(uid):
        '''
        删除redis中的jwt_token
        '''
        user = get_table(table=User, execute='get', id=uid)
        if isinstance(user, dict):
            return jsonify(response_return(1, user))
        try:
            Redis.delete('jwt_' + user.mobile)
        except Exception:
            return jsonify(response_return(1, u'jwt_token删除失败'))

    @classmethod
    def jwt_token_verify(cls):
        '''
        jwt_token认证
        :return: dict
        '''
        # 格式Authorization: JWT jwt_token
        try:
            auth_header = request.headers.get('Authorization').encode()
        except Exception:
            return response_return(2, u'获取Authorization失败')
        if not auth_header:
            return response_return(2, u'没有提供token')
        jwt_tokenArr = auth_header.split(" ")
        if not all([jwt_tokenArr, jwt_tokenArr[0] == 'JWT', len(jwt_tokenArr) ==2]):
            return response_return(2, u'请传递正确的验证头信息')
        jwt_token = jwt_tokenArr[1]
        response_data =cls.decode_jwt_token(jwt_token)
        payload = response_data.get('data')
        if not payload:
            return response_data
        try:
            user = User.query.get(payload['data']['id'])
        except Exception:
            return response_return(2, u'数据查询失败')
        if not user:
            return response_return(2, u'该用户不存在')
        if (user.login_time.strftime("%Y-%m-%d %H:%M:%S") != payload['data']['login_time']):
            return response_return(2, u'Token已更改, 请重新登录')
        # 用户信息是否被后台管理员或用户修改过
        if (user.lastchange.strftime("%Y-%m-%d %H:%M:%S") != payload['data']['lastchange']):
            return response_return(2, u'用户信息已修改，请重新登录')
        # 查询redis是否有登录用户的jwt_token
        try:
            if not Redis.exists('jwt_' + user.mobile):
                return response_return(2, u'请登录后访问')
        except Exception:
            return response_return(1, u'redis错误')
        g.user_id = payload['data']['id']
        g.managerList = payload['data']['managerList']
        return response_return(0, u'token验证通过')

    @classmethod
    def required(cls, manager_list=None, endpoint=None):
        '''
        鉴权
        1 部门管理员：可以编辑本部门任意同事本月，下月排班表；
            不能编辑其他部门信息、导出值班表、本月之前值班信息、
        2 业务管理员：可以导出值班表，确定建群默认添加人员，不需要发送短信人员，人工触发建群，人工发送短信
        维护值班提醒内容。无其他权限
        3 超级管理员：默认拥有所有权限
        4 查看值班表默认对所有人开放
        '''
        def wrapper(fn):
            @functools.wraps(fn)
            def decorated_view(*args, **kwargs):
                # 公开访问资源
                if request.method == 'GET' and request.endpoint == endpoint:
                    return fn(*args, **kwargs)
                # 判断登录用户
                response_data = cls.jwt_token_verify()
                if response_data['code']:
                    return jsonify(response_data)
                # 用户所在管理组
                managerList = g.managerList
                if not managerList:
                    return jsonify(response_return(3, u'没有权限访问'))
                # 超级管理组
                S_MANAGEMENT = 'S_MANAGEMENT'
                if S_MANAGEMENT in managerList:
                    return fn(*args, **kwargs)
                # 该访问用户所拥有的权限
                u_permissions = []
                for m in managerList:
                    try:
                        manager = Management.query.filter_by(name=m).first()
                    except Exception:
                        return jsonify(response_return(3, u'数据查询失败'))
                    u_p = get_table(result=response_return(), execute='relationship', relationship=(manager.permissions))
                    if isinstance(u_p, dict) or isinstance(manager, dict):
                        return jsonify(response_return(3, u'u_p或manager数据查询失败'))
                    u_permissions.extend(u_p)
                # 访问部门资源
                module_departId = request.values.get('departId')
                if module_departId:
                    # 访问此接口所需要的权限
                    depart = get_table(result=response_return(), table=Department,
                                              execute='get', id=module_departId
                                              )
                    if isinstance(depart, dict):
                        return jsonify(response_return(3, u'部门数据查询失败或无部门信息'))
                    d_permissions = depart.permissions.all()
                    d_u_permissions = [p for p in u_permissions if p in d_permissions]
                    if not d_u_permissions:
                        return jsonify(response_return(3, u'没有权限访问'))
                    allow_method = [ p for p in d_u_permissions if p.codename == request.method]
                    if not allow_method:
                        return jsonify(response_return(3, u'没有权限访问'))
                    return fn(*args, **kwargs)
                # 访问非部门资源
                if manager_list:
                    allow_manager = [m for m in manager_list if m in managerList]
                    if not allow_manager:
                        return jsonify(response_return(3, u'没有权限访问'))
                    return fn(*args, **kwargs)
                return jsonify(response_return(3, u'没有权限访问'))
            return decorated_view
        return wrapper
