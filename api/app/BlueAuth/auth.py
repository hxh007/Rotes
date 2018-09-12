# coding=utf-8

import jwt, datetime
from flask import jsonify

import config
from app import Redis
from app.BlueAuth.common import response_return, get_table
from app.models import User
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
                return payload
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
