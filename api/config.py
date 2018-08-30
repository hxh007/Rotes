# coding=utf-8
import os, sys


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 添加模块加载路径
    sys.path.append(basedir)
    # 调试模式
    DEBUG = None
    # 配置秘钥
    SECRET_KEY = 'Xi37bWtclV4ThL42+MTCZppEOc/MuDR8V2gX5888XZ0='

    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, "datas", "app-dev.sqlite3")
    # 数据库动态追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    # 开启调试模式
    DEBUG = True


class ProductionConfig(Config):
    # 关闭调试模式
    DEBUG = False

config = {
    "dev_config": DevelopmentConfig,
    "pro_config": ProductionConfig
}
