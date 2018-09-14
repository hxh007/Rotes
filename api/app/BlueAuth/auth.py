# coding=utf-8

import jwt, datetime
from flask import jsonify, request

import config
from app import Redis
from app.BlueAuth.common import response_return, get_table
from app.models import User, Management
from .constants import JWT_EXP_DAYS, JWT_EXP_SECONDS

class Authentication():

    @staticmethod
    def encode_jwt_token(user, managerList):
        '''
        生成认证Token
        :return:jwt_token
        '''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXP_DAYS, seconds=JWT_EXP_SECONDS), # 过期时间
                'iat': datetime.datetime.utcnow(), # 签发时间
                'iss': 'auth', # 签发人
                'data':{
                    'id': user.id,
                    'manager': managerList,
                    'login_time': user.login_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'lastchange': user.lastchange.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            return jwt.encode(
                payload,
                config.Config.SECRET_KEY,
                algorithm='HS256'
                )
        except Exception as e:
            return e

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
                return response_return(1, u'无效token')
        except Exception:
            return response_return(1, u'无效token')

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

    def jwt_token_verify(self):
        '''
        jwt_token认证
        :return: dict
        '''
        # 格式Authorization: JWT jwt_token
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response_return(1, u'没有提供token')
        jwt_tokenArr = auth_header.split("")
        if not all([jwt_tokenArr, jwt_tokenArr[0] == 'JWT', len(jwt_tokenArr) ==2]):
            return response_return(1, u'请传递正确的验证头信息')
        jwt_token = jwt_tokenArr[1]
        response_data = self.decode_jwt_token(jwt_token)
        payload = response_data.get('data')
        if not payload:
            return response_data
        try:
            user = User.query.get(payload['data']['id'])
        except Exception:
            return response_return(1, u'数据查询失败')
        if not user:
            return response_return(1, u'该用户不存在')
        if (user.login_time != payload['data']['login_time']):
            return response_return(1, u'Token已更改, 请重新登录')
        # 用户信息是否被后台管理员或用户修改过
        if (user.lastchange != payload['data']['lastchange']):
            return response_return(1, u'用户信息已修改，请重新登录')
        # 查询redis是否有登录用户的jwt_token
        if not Redis.exists('jwt_' + user.mobile):
            return response_return(1, u'请登录后访问')
        return response_return(0, u'token验证通过', manager=payload.get('manager'))

    def required(self, module_management):
        '''
        鉴权
        1 部门管理员：可以编辑本部门任意同事本月，下月排班表；
            不能编辑其他部门信息、导出值班表、本月之前值班信息、
        2 业务管理员：可以导出值班表，确定建群默认添加人员，不需要发送短信人员，人工触发建群，人工发送短信
        维护值班提醒内容。无其他权限
        3 超级管理员：默认拥有所有权限
        4 查看值班表默认对所有人开放
        '''
        response_data = self.jwt_token_verify()
        manager = response_data.get('manager', None)
        if not manager:
            return jsonify(1, u'没有权限访问')\
        # 该访问用户所拥有的权限
        u_permissions = []
        for m in manager:
            u_p = get_table(result=response_return(), table=Management, execute='relationship', relationship=Management.permissions)
            u_permissions.extend(u_p)
        
        pass
