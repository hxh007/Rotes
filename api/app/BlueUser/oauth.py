# coding=utf-8

from urllib import urlencode, unquote

import requests

from app.BlueAuth.common import response_return
from app.BlueUser import constants


class OAuthDD(object):
    '''钉钉登录工具类
    https://oapi.dingtalk.com/connect/qrconnect?appid=dingoarzgcktudlqsgvyjn&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=http://127.0.0.1
    '''
    def __init__(self, appid=None, appsecret=None, redirect_uri=None, state=None, scope=None):
        '''构造方法，需要使用到的参数'''
        self.appid = appid or constants.APPID
        self.appsecret = appsecret or constants.APPSECRET
        self.redirect_uri = redirect_uri or constants.REDIRECT_URI
        self.state = state or constants.STATE
        self.scope = scope or constants.SCOPE

    def get_dd_login_params(self):
        '''钉钉扫码登录参数'''

        # 准备参数
        params = {
            'appid': self.appid, # 钉钉应用唯一标识
            'response_type': 'code', # 扫码标识
            'redirect_uri': self.redirect_uri, # 扫码成功后跳转到的页面
            'state': self.state, # 防止重放攻击 登录成功后跳转到的页面
            'scope':'snsapi_login' #
        }

        return params

    def get_access_token(self):
        '''通过appid和appsecret获取access_token'''

        # 准备url
        url = 'https://oapi.dingtalk.com/sns/gettoken?'
        # 准备参数
        params = {
            'appid': self.appid,
            'appsecret': self.appsecret
        }
        try:
            # 向钉钉服务器发送请求获取access_token
            response = requests.get(url, params=params)
            # 对response进行处理 获取access_token
            access_token = response.json().get('access_token')
        except Exception:
            return response_return(1, u'获取access_token失败')
        return access_token

    def get_persistent_code(self, access_token, code):
        '''通过accesstoken和code(tmp_auth_code)获取永久授权码'''
        # 准备url
        url = 'https://oapi.dingtalk.com/sns/get_persistent_code'
        # 准备参数
        params = {
            'access_token': access_token,
        }
        json = {
            'tmp_auth_code': code
        }
        try:
            # 向钉钉服务器发送请求获取persistent_code
            response = requests.post(url, params=params, json=json)
            # 对response进行处理 获取persistent_token
            persistent_code_dict= response.json()
            openid = persistent_code_dict.get('openid')
            persistent_code = persistent_code_dict.get('persistent_code')
        except Exception:
            return response_return(1, u'获取永久授权码失败')
        return [openid, persistent_code]

    def get_sns_token(self, access_token, openid, persistent_code):
        '''通过access_token获取sns_token'''
        # 准备url
        url = 'https://oapi.dingtalk.com/sns/get_sns_token'
        # 准备参数
        params = {
            'access_token': access_token
        }
        json = {
            "openid": openid,
            "persistent_code": persistent_code
        }
        try:
            # 向钉钉服务器发送请求获取sns_token
            response = requests.post(url, params=params, json=json)
            # 数据处理
            sns_token = response.json().get('sns_token')
        except Exception:
            return response_return(1, u'获取sns_token失败')
        return sns_token

    def get_dd_user(self, sns_token):
        '''通过sns_token获取钉钉用户信息'''
        # url准备
        url = 'https://oapi.dingtalk.com/sns/getuserinfo'
        # 准备参数
        params = {
            'sns_token': sns_token,
        }
        try:
            # 向钉钉服务器发送请求获取用户信息
            response = requests.get(url, params=params)
            user_info = response.json().get('user_info')
        except Exception:
            return response_return(1, u'获取钉钉用户信息失败')
        return user_info
