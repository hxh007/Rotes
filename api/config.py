# coding=utf-8
import ConfigParser
import os, sys

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class Config(object):
    # api 作为根路径
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 将api加入到导入路径中
    sys.path.append(basedir)
    # 调试模式
    DEBUG = None
    # 配置秘钥
    SECRET_KEY = 'Xi37bWtclV4ThL42+MTCZppEOc/MuDR8V2gX5888XZ0='

    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, "datas", "app-dev.sqlite3")
    # Excel文件路径
    Excel_path = os.path.join(basedir, 'app', 'static')
    # 数据库动态追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 跨域白名单
    CORS_URL = '*'

    # 配置redis
    conf = ConfigParser.RawConfigParser()
    conf.read(os.path.join(basedir, 'config.ini'))

    REDIS_HOST = conf.get('redis', 'host')
    REDIS_PORT = conf.get('redis', 'port')
    REDIS_PASSWORD = conf.get('redis', 'pwd')
    REDIS_DB = conf.get('redis', 'redis_exchange')
    REDIS_CACHE_DB = conf.get('redis', 'redis_cache')
    CACHE_TYPE = conf.get('redis', 'cache_type')
    CACHE_KEY_PREFIX = conf.get('redis', 'cache_key_prefix')
    REDIS_MAX_CONNECTIONS = conf.get('redis', 'redis_exchange')

    # apscheduler配置项
    SCHEDULER_JOBSTORES = {
        'default':SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }
    SCHEDULER_EXECUTORS = {
        'default':{'type':'threadpool', 'max_workers':9}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce':False,
        'max_instances':3
    }
    SCHEDULER_API_ENABLED = False

    # 漫道短信接口配置
    SMS_SN = conf.get('sms', 'sn')
    SMS_PW = conf.get('sms', 'pw')                
    SMS_GW = conf.get('sms', 'gw')

    # 钉钉建群接口配置
    DING_GW = conf.get('ding', 'gw')
    DING_DEFAULT_OWNER = conf.get('ding', 'default_owner')

    # 钉钉扫码登录接口配置
    APPSECRET = conf.get('ding_login', 'appsecret')
    REDIRECT_URI = conf.get('ding_login', 'redirect_uri')
    STATE = conf.get('ding_login', 'state')
    SCOPE = conf.get('ding_login', 'scope')
    APPID = conf.get('ding_login', 'appid')
    CORPID = conf.get('ding_login', 'corpid')
    CORPSECRET = conf.get('ding_login', 'corpsecret')


class DevelopmentConfig(Config):
    # 开启调试模式
    DEBUG = True


class TestConfig(Config):
    # 开启测试模式
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(Config.basedir, "datas", "app-tests.sqlite3")


class ProductionConfig(Config):
    # 关闭调试模式
    DEBUG = False


config = {
    "dev_config": DevelopmentConfig,
    "test_config": TestConfig,
    "pro_config": ProductionConfig
}
